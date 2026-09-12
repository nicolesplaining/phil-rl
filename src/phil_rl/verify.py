"""Diagnostic checks on a fixed formalization, never a reward for translation fidelity."""

import z3

from phil_rl.logic import Z3Compiler, parse
from phil_rl.schema import Artifact


def finite_counterexample(formalization, translations, premise_ids, conclusion_id, timeout_ms):
    """A finite SAT witness refutes entailment. Finite UNSAT proves nothing here."""
    for size in range(1, 4):
        compiler = Z3Compiler(formalization, domain_size=size)
        try:
            premises = [compiler.compile(parse(translations[c])) for c in premise_ids]
            conclusion = compiler.compile(parse(translations[conclusion_id]))
        except ValueError:
            return None
        solver = z3.Solver()
        solver.set(timeout=max(1, timeout_ms // 3))
        solver.add(*premises, z3.Not(conclusion))
        if solver.check() == z3.sat:
            return {
                "status": "invalid",
                "premises_satisfiable": True,
                "countermodel": str(solver.model()),
                "countermodel_domain_size": size,
                "countermodel_search": "finite witness, without assuming the domain is finite",
            }
    return None


def check(artifact: Artifact, include_implicit: bool = False, timeout_ms: int = 5000) -> dict:
    if timeout_ms <= 0:
        raise ValueError("Solver timeout must be positive.")
    artifact = Artifact.model_validate(artifact.model_dump())
    reconstruction, formalization = artifact.reconstruction, artifact.formalization
    premise_ids = reconstruction.premise_ids(include_implicit)
    translations = {t.claim_id: t.formula for t in formalization.translations}
    needed = premise_ids + [reconstruction.conclusion_id]
    base = {
        "formalization_sha256": artifact.formalization_sha256,
        "reconstruction_sha256": artifact.reconstruction_sha256,
        "included_premise_ids": premise_ids,
        "includes_implicit_premises": include_implicit,
        "fidelity": "not_assessed",
        "lean_proof_checked": False,
        "solver": f"z3 {z3.get_version_string()}",
    }
    if formalization.logic == "unsupported" or any(translations[c] is None for c in needed):
        return {
            **base,
            "status": "unsupported",
            "reason": "An active claim lacks a supported formula.",
        }
    if formalization.logic == "classical_first_order":
        witness = finite_counterexample(
            formalization,
            translations,
            premise_ids,
            reconstruction.conclusion_id,
            min(timeout_ms, 300),
        )
        if witness:
            return {**base, **witness}
    compiler = Z3Compiler(formalization)
    try:
        formulas = {c: compiler.compile(parse(translations[c])) for c in needed}
    except ValueError as error:
        return {**base, "status": "unknown", "reason": str(error)}
    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    solver.add(*(formulas[c] for c in premise_ids))
    consistency = solver.check()
    if consistency == z3.unsat:
        return {**base, "status": "inconsistent_premises", "premises_satisfiable": False}
    if consistency == z3.unknown:
        return {**base, "status": "unknown", "reason": solver.reason_unknown()}
    solver.add(z3.Not(formulas[reconstruction.conclusion_id]))
    result = solver.check()
    if result == z3.sat:
        model = solver.model()
        assignments = {
            s.name: str(model.eval(compiler.symbols[s.name], model_completion=True))
            for s in formalization.symbols
            if s.kind != "predicate"
        }
        return {
            **base,
            "status": "invalid",
            "premises_satisfiable": True,
            "countermodel": str(model),
            "assignments": assignments,
        }
    if result == z3.unknown:
        return {**base, "status": "unknown", "reason": solver.reason_unknown()}
    tautology = z3.Solver()
    tautology.set(timeout=timeout_ms)
    tautology.add(z3.Not(formulas[reconstruction.conclusion_id]))
    warnings = []
    if tautology.check() == z3.unsat:
        warnings.append("The conclusion is a tautology in the selected logic.")
    for premise in premise_ids:
        if parse(translations[premise]) == parse(translations[reconstruction.conclusion_id]):
            warnings.append(f"Premise {premise} repeats the conclusion's formula.")
    return {
        **base,
        "status": "valid",
        "premises_satisfiable": True,
        "warnings": warnings,
        "qualification": "Entailment under this encoding; English fidelity remains unassessed.",
    }
