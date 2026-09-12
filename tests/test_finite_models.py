import z3

from phil_rl.examples import fixtures
from phil_rl.logic import Z3Compiler, parse
from phil_rl.verify import check, finite_counterexample


def test_finite_unsat_never_certifies_validity():
    artifact = fixtures()["syllogism"][0]
    result = finite_counterexample(
        artifact.formalization,
        {t.claim_id: t.formula for t in artifact.formalization.translations},
        artifact.reconstruction.premise_ids(),
        artifact.reconstruction.conclusion_id,
        300,
    )
    assert result is None


def test_quantifier_scope_has_a_finite_counterexample():
    result = check(fixtures()["scope"][0])
    assert result["status"] == "invalid"
    assert 1 <= result["countermodel_domain_size"] <= 3


def test_quantifier_grounding_covers_every_domain_element():
    artifact = fixtures()["scope"][0]
    compiler = Z3Compiler(artifact.formalization, domain_size=2)
    formula = compiler.compile(parse("(forall x (exists y (Admires x y)))"))
    assert z3.is_and(formula) and formula.num_args() == 2
    assert all(z3.is_or(child) and child.num_args() == 2 for child in formula.children())


def test_unknown_solver_never_yields_a_positive_result(monkeypatch):
    monkeypatch.setattr(z3.Solver, "check", lambda self: z3.unknown)
    monkeypatch.setattr(z3.Solver, "reason_unknown", lambda self: "test timeout")
    result = check(fixtures()["scope"][0], timeout_ms=1)
    assert result["status"] == "unknown"
    assert result["reason"] == "test timeout"
