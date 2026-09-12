import pytest

from phil_rl.examples import fixtures
from phil_rl.policy import explicit_only, normalized_formalization
from phil_rl.schema import Formalization, Reconstruction
from phil_rl.source import GroundedReconstruction


def test_outcome_and_reason_are_required_in_model_schema():
    required = GroundedReconstruction.model_json_schema()["required"]
    assert "status" in required and "reason" in required


def test_proposed_premises_are_not_allowed_in_default_extraction():
    with pytest.raises(ValueError, match="explicit-only"):
        explicit_only(fixtures()["missing_bridge"][0].reconstruction)


def test_attribution_is_not_the_content_of_an_objection():
    data = fixtures()["modus_ponens"][0].reconstruction.model_dump()
    data["claims"][0].update(role="objection", text="A critic says the agent acted freely.")
    with pytest.raises(ValueError, match="reporting frame"):
        explicit_only(Reconstruction.model_validate(data))


def test_nonassumption_reply_cannot_hide_a_supporting_claim():
    data = fixtures()["modus_ponens"][0].reconstruction.model_dump()
    data["claims"][0]["role"] = "reply"
    with pytest.raises(ValueError, match="logical role"):
        explicit_only(Reconstruction.model_validate(data))


def test_background_roles_do_not_excuse_incomplete_translation():
    ref = fixtures()["modus_ponens"][0]
    data = ref.formalization.model_dump()
    data["translations"][0].update(formula=None, reason="This is context.")
    with pytest.raises(ValueError, match="every claim needs a formula"):
        normalized_formalization(ref.reconstruction, Formalization.model_validate(data))


def test_unused_symbols_are_rejected_without_proof_feedback():
    ref = fixtures()["modus_ponens"][0]
    data = ref.formalization.model_dump()
    data["symbols"].append(
        {"name": "Unused", "kind": "proposition", "arity": 0, "meaning": "Unused declaration"}
    )
    with pytest.raises(ValueError, match="Unused glossary"):
        normalized_formalization(ref.reconstruction, Formalization.model_validate(data))


def test_fol_domain_cannot_silently_imply_class_existence():
    ref = fixtures()["existential_import"][0]
    with pytest.raises(ValueError, match="noun restrictions"):
        normalized_formalization(ref.reconstruction, ref.formalization)


def test_defeasible_qualifier_cannot_become_a_strict_rule():
    ref = fixtures()["modus_ponens"][0]
    data = ref.reconstruction.model_dump()
    data["claims"][0]["text"] = "Usually responsibility implies freedom."
    with pytest.raises(ValueError, match="qualifier"):
        normalized_formalization(Reconstruction.model_validate(data), ref.formalization)


def test_explicit_negative_atoms_require_operator_normalization():
    ref = fixtures()["modus_ponens"][0]
    data = ref.formalization.model_dump()
    data["symbols"][0]["meaning"] = "The agent is not responsible."
    with pytest.raises(ValueError, match="embeds explicit negation"):
        normalized_formalization(ref.reconstruction, Formalization.model_validate(data))


@pytest.mark.parametrize(
    "wording",
    [
        "If the witness had spoken, the trial would have ended.",
        "The agent could not have done otherwise.",
        "Necessarily this statement holds.",
        "Tao knows that the statement holds.",
    ],
)
def test_unsupported_operators_cannot_be_silently_flattened(wording):
    ref = fixtures()["modus_ponens"][0]
    data = ref.reconstruction.model_dump()
    data["claims"][0]["text"] = wording
    with pytest.raises(ValueError, match="unsupported qualifier"):
        normalized_formalization(Reconstruction.model_validate(data), ref.formalization)


def test_builtin_equality_does_not_need_a_glossary_declaration():
    ref = fixtures()["syllogism"][0]
    data = ref.formalization.model_dump()
    data["domain_description"] = "All individuals."
    normalized_formalization(ref.reconstruction, Formalization.model_validate(data))
