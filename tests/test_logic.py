import pytest

from phil_rl.examples import fixtures
from phil_rl.lean import export
from phil_rl.logic import parse, validate_expr
from phil_rl.schema import Artifact, Evidence, fingerprint
from phil_rl.verify import check


@pytest.mark.parametrize("name", list(fixtures()))
def test_reference_outcomes(name):
    artifact, explicit, augmented = fixtures()[name]
    assert check(artifact)["status"] == explicit
    assert check(artifact, True)["status"] == augmented


def test_countermodel_and_separate_implicit_premises():
    artifact = fixtures()["missing_bridge"][0]
    before = fingerprint(artifact)
    explicit, augmented = check(artifact), check(artifact, True)
    assert explicit["assignments"] == {"R": "True", "F": "False"}
    assert "bridge" not in explicit["included_premise_ids"]
    assert "bridge" in augmented["included_premise_ids"]
    assert fingerprint(artifact) == before
    assert explicit["fidelity"] == "not_assessed"
    assert not explicit["lean_proof_checked"]


def test_circularity_is_a_warning_not_philosophical_success():
    result = check(fixtures()["circular"][0])
    assert result["status"] == "valid"
    assert any("repeats" in warning for warning in result["warnings"])


@pytest.mark.parametrize(
    "formula",
    [
        "",
        "(and P)",
        "(and P Q R)",
        "(not P Q)",
        "Q P",
        "(not P",
        "(P)",
        "P;import",
        "(forall x (Human x))",
    ],
)
def test_rejects_bad_formulas(formula):
    artifact = fixtures()["modus_ponens"][0]
    symbols = {s.name: s for s in artifact.formalization.symbols}
    with pytest.raises(ValueError):
        validate_expr(parse(formula), symbols, "classical_propositional")


@pytest.mark.parametrize(
    "formula",
    [
        "(Human x)",
        "(Human socrates socrates)",
        "(forall socrates (Human socrates))",
        "(exists x (forall x (Human x)))",
        "(eq Human socrates)",
    ],
)
def test_rejects_ill_scoped_fol(formula):
    artifact = fixtures()["syllogism"][0]
    with pytest.raises(ValueError):
        validate_expr(
            parse(formula),
            {s.name: s for s in artifact.formalization.symbols},
            "classical_first_order",
        )


def test_evidence_is_exact_and_offsets_handle_unicode_and_duplicates():
    source = "自由. P. P."
    assert Evidence(quote="P.", occurrence=1).locate(source) == (7, 9)
    with pytest.raises(ValueError):
        Evidence(quote="p.", occurrence=0).locate(source)
    with pytest.raises(ValueError):
        Evidence(quote="P.", occurrence=2).locate(source)


def test_integrity_rejects_changed_artifacts():
    artifact = fixtures()["modus_ponens"][0].model_dump()
    artifact["formalization"]["translations"][-1]["formula"] = "R"
    with pytest.raises(ValueError, match="fingerprint mismatch"):
        Artifact.model_validate(artifact)


def test_subconclusions_are_not_premises():
    original = fixtures()["modus_ponens"][0]
    data = original.reconstruction.model_dump()
    data["claims"][0]["role"] = "subconclusion"
    reconstruction = type(original.reconstruction).model_validate(data)
    artifact = Artifact.create(original.source, reconstruction, original.formalization)
    assert check(artifact)["included_premise_ids"] == ["c2"]
    assert check(artifact)["status"] == "invalid"


def test_objections_are_not_premises():
    original = fixtures()["modus_ponens"][0]
    data = original.reconstruction.model_dump()
    data["claims"][0]["role"] = "objection"
    reconstruction = type(original.reconstruction).model_validate(data)
    artifact = Artifact.create(original.source, reconstruction, original.formalization)
    assert check(artifact)["status"] == "invalid"


def test_lean_export_distinguishes_statement_and_proof():
    artifact = fixtures()["modus_ponens"][0]
    statement, proof = export(artifact), export(artifact, prove=True)
    assert "def argumentStatement" in statement and "theorem" not in statement
    assert "theorem argumentProof" in proof and "#print axioms argumentProof" in proof
    assert "sorry" not in proof and "axiom " not in proof
    assert "[Nonempty Domain]" in export(fixtures()["syllogism"][0])
    for name in ["inconsistent", "affirming_consequent", "modal", "syllogism"]:
        with pytest.raises(ValueError):
            export(fixtures()[name][0], prove=True)


def test_unconnected_premises_do_not_enter_check():
    original = fixtures()["modus_ponens"][0]
    data = original.reconstruction.model_dump()
    data["relations"] = []
    reconstruction = type(original.reconstruction).model_validate(data)
    artifact = Artifact.create(original.source, reconstruction, original.formalization)
    assert check(artifact)["included_premise_ids"] == []
    assert check(artifact)["status"] == "invalid"


def test_bound_variables_cannot_capture_declared_constants():
    import z3

    from phil_rl.logic import Z3Compiler
    from phil_rl.schema import Symbol

    formalization = fixtures()["syllogism"][0].formalization.model_copy(
        update={
            "symbols": [
                Symbol(name="bound_x", kind="constant", arity=0, meaning="A fixed object.")
            ],
        }
    )
    compiler = Z3Compiler(formalization)
    formula = compiler.compile(parse("(forall x (eq x bound_x))"))
    solver = z3.Solver()
    solver.add(z3.Not(formula))
    assert solver.check() == z3.sat
