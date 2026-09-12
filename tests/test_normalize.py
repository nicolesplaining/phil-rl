from pathlib import Path

import pytest
import z3

from phil_rl.examples import fixtures, make
from phil_rl.logic import Z3Compiler, parse
from phil_rl.normalize import ground_abstraction
from phil_rl.schema import Artifact, Formalization
from phil_rl.verify import check


def ground_example():
    return make(
        "Ground predicates",
        ["If Ari is sincere, Ari is candid.", "Ari is sincere."],
        "Therefore Ari is candid.",
        ["(implies (Sincere ari) (Candid ari))", "(Sincere ari)", "(Candid ari)"],
        [
            ("Sincere", "predicate", 1, "x is sincere"),
            ("Candid", "predicate", 1, "x is candid"),
            ("ari", "constant", 0, "Ari"),
        ],
        logic="classical_first_order",
    )


def test_ground_abstraction_preserves_every_formula_under_its_definitions():
    artifact = ground_example()
    normalized, trace = ground_abstraction(artifact.formalization)
    assert normalized.logic == "classical_propositional"
    assert trace["inverse_substitution_checked"]
    assert len(normalized.symbols) == 2
    original_compiler = Z3Compiler(artifact.formalization)
    projected_compiler = Z3Compiler(normalized)
    definitions = [
        projected_compiler.symbols[name] == original_compiler.compile(parse(formula))
        for name, formula in trace["atoms"].items()
    ]
    for original, projected in zip(
        artifact.formalization.translations, normalized.translations, strict=True
    ):
        solver = z3.Solver()
        solver.add(
            *definitions,
            original_compiler.compile(parse(original.formula))
            != projected_compiler.compile(parse(projected.formula)),
        )
        assert solver.check() == z3.unsat
    result = Artifact.create(artifact.source, artifact.reconstruction, normalized)
    assert check(result)["status"] == check(artifact)["status"] == "valid"


@pytest.mark.parametrize("name", ["scope", "syllogism", "existential_import", "modal"])
def test_quantifiers_and_unsupported_logic_are_not_abstracted(name):
    original = fixtures()[name][0].formalization
    normalized, trace = ground_abstraction(original)
    assert normalized == original and trace is None


def test_equality_is_not_abstracted_into_an_independent_atom():
    data = ground_example().formalization.model_dump()
    data["translations"][0]["formula"] = "(eq ari ari)"
    original = Formalization.model_validate(data)
    normalized, trace = ground_abstraction(original)
    assert normalized == original and trace is None


@pytest.mark.parametrize("case", ["q12", "q14", "q16"])
def test_ground_heldout_variants_preserve_their_original_status(case):
    path = Path(__file__).parents[1] / "experiments" / "heldout-v2" / case / "argument.json"
    artifact = Artifact.model_validate_json(path.read_text())
    formalization, trace = ground_abstraction(artifact.formalization)
    assert trace and formalization.logic == "classical_propositional"
    projected = Artifact.create(artifact.source, artifact.reconstruction, formalization)
    assert check(projected)["status"] == check(artifact)["status"]
