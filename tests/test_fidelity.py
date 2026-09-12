from pathlib import Path

import pytest

from phil_rl.benchmark import load_suite, reference
from phil_rl.examples import fixtures
from phil_rl.fidelity import MeaningReview, assess
from phil_rl.schema import Artifact, Formalization, Reconstruction, fingerprint


def review_for(ref, generated=None, **kwargs):
    generated = generated or ref
    return MeaningReview(
        reference_sha256=fingerprint(ref),
        generated_sha256=fingerprint(generated),
        reviewer_kind="test_fixture",
        symbol_map={s.name: s.name for s in generated.formalization.symbols},
        glossary_rationale="Fixture uses the same English glossary.",
        claims=[
            {"reference_ids": [c.id], "generated_ids": [c.id]}
            for c in ref.reconstruction.claims
            if c.origin == "explicit"
        ],
        source_meaning_approved=True,
        source_review_notes="Deliberately aligned test fixture.",
        **kwargs,
    )


def rebuild(ref, data):
    return Artifact.create(
        ref.source,
        Reconstruction.model_validate(data["reconstruction"]),
        Formalization.model_validate(data["formalization"]),
    )


def test_identical_reference_passes_reviewed_alignment():
    ref = fixtures()["modus_ponens"][0]
    assert assess(ref, ref, review_for(ref))["status"] == "passed_under_reviewed_alignment"


def test_same_validity_does_not_hide_changed_formulas():
    ref = fixtures()["modus_ponens"][0]
    data = ref.model_dump()
    data["formalization"]["translations"][0]["formula"] = "(implies F R)"
    data["formalization"]["translations"][1]["formula"] = "F"
    data["formalization"]["translations"][2]["formula"] = "R"
    generated = rebuild(ref, data)
    result = assess(ref, generated, review_for(ref, generated))
    assert result["status"] == "not_passed"
    assert all(c["formula_comparison"] == "not_equivalent" for c in result["claim_groups"])


def test_correct_formulas_do_not_hide_dropped_active_premise():
    ref = fixtures()["modus_ponens"][0]
    data = ref.model_dump()
    data["reconstruction"]["relations"][0]["premises"] = ["c1"]
    generated = rebuild(ref, data)
    result = assess(ref, generated, review_for(ref, generated))
    assert result["active_premises"] == "not_equivalent"


def test_review_cannot_be_reused_after_reconstruction_changes():
    ref = fixtures()["modus_ponens"][0]
    data = ref.model_dump()
    data["reconstruction"]["claims"][0]["text"] = "Changed meaning."
    with pytest.raises(ValueError, match="fingerprints"):
        assess(ref, rebuild(ref, data), review_for(ref))


def test_unapproved_source_meaning_never_passes():
    ref = fixtures()["modus_ponens"][0]
    review = review_for(ref).model_copy(update={"source_meaning_approved": False})
    assert assess(ref, ref, review)["status"] == "not_passed"


def test_narrow_domain_accounts_for_constants_and_nonemptiness():
    suite = load_suite(Path(__file__).parents[1] / "benchmarks" / "heldout-v1.json")
    ref = reference(next(c for c in suite["cases"] if c["id"] == "h25"))
    data = ref.model_dump()
    data["formalization"]["domain_description"] = "People."
    data["formalization"]["symbols"] = [
        s for s in data["formalization"]["symbols"] if s["name"] != "Person"
    ]
    data["formalization"]["translations"][0]["formula"] = (
        "(forall x (implies (Consents x) (Informed x)))"
    )
    data["formalization"]["translations"][1]["formula"] = "(Consents mira)"
    generated = rebuild(ref, data)
    result = assess(ref, generated, review_for(ref, generated, domain_restriction="Person"))
    assert result["status"] == "passed_under_reviewed_alignment"


def test_narrow_domain_cannot_hide_existential_import():
    suite = load_suite(Path(__file__).parents[1] / "benchmarks" / "heldout-v1.json")
    ref = reference(next(c for c in suite["cases"] if c["id"] == "h26"))
    data = ref.model_dump()
    data["formalization"]["domain_description"] = "Perfect judges."
    data["formalization"]["symbols"] = [
        s for s in data["formalization"]["symbols"] if s["name"] != "PerfectJudge"
    ]
    data["formalization"]["translations"][0]["formula"] = "(forall x (Impartial x))"
    data["formalization"]["translations"][1]["formula"] = "(exists x (Impartial x))"
    generated = rebuild(ref, data)
    result = assess(ref, generated, review_for(ref, generated, domain_restriction="PerfectJudge"))
    assert result["active_premises"] == "not_equivalent"
