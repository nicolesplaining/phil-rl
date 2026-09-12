"""Lossless Boolean abstraction of ground FOL without quantifiers or equality."""

from phil_rl.logic import Expr, parse
from phil_rl.schema import Formalization, Symbol, Translation, fingerprint


def render(expr: Expr) -> str:
    return f"({expr.op} {' '.join(render(a) for a in expr.args)})" if expr.args else expr.op


def ground_abstraction(formalization: Formalization):
    if formalization.logic != "classical_first_order" or any(
        t.formula is None for t in formalization.translations
    ):
        return formalization, None
    originals = {t.claim_id: parse(t.formula) for t in formalization.translations}

    def eligible(expr):
        return expr.op not in {"forall", "exists", "eq"} and all(eligible(a) for a in expr.args)

    if not all(eligible(expr) for expr in originals.values()):
        return formalization, None
    symbols = {s.name: s for s in formalization.symbols}
    generated = [s for s in formalization.symbols if s.kind == "proposition"]
    atoms = {}

    def abstract(expr):
        if expr.op in symbols and symbols[expr.op].kind == "predicate":
            if expr not in atoms:
                counter = len(atoms) + 1
                name = f"GroundAtom{counter}"
                while name in symbols or any(s.name == name for s in generated):
                    counter += 1
                    name = f"GroundAtom{counter}"
                atoms[expr] = name
                arguments = "; ".join(f"{a.op}: {symbols[a.op].meaning}" for a in expr.args)
                meaning = (
                    f"{render(expr)}. Predicate meaning: {symbols[expr.op].meaning}. "
                    f"Arguments: {arguments}"
                )
                generated.append(Symbol(name=name, kind="proposition", arity=0, meaning=meaning))
            return Expr(atoms[expr])
        return Expr(expr.op, tuple(abstract(a) for a in expr.args))

    try:
        projected = {key: abstract(expr) for key, expr in originals.items()}
    except ValueError:
        return formalization, None
    if len(generated) > 128:
        return formalization, None
    inverse = {name: expr for expr, name in atoms.items()}

    def restore(expr):
        return inverse.get(expr.op, Expr(expr.op, tuple(restore(a) for a in expr.args)))

    if any(restore(projected[key]) != value for key, value in originals.items()):
        raise ValueError("Ground abstraction failed its structural round-trip check.")
    try:
        result = Formalization(
            logic="classical_propositional",
            domain_description="Ground statements with original predicate meanings retained.",
            symbols=generated,
            translations=[
                Translation(
                    claim_id=t.claim_id, formula=render(projected[t.claim_id]), reason=t.reason
                )
                for t in formalization.translations
            ],
            interpretation_notes=formalization.interpretation_notes,
        )
    except ValueError:
        return formalization, None
    return result, {
        "kind": "ground_boolean_abstraction",
        "version": "0.1",
        "original_formalization": formalization.model_dump(),
        "original_sha256": fingerprint(formalization),
        "atoms": {name: render(expr) for name, expr in inverse.items()},
        "inverse_substitution_checked": True,
        "qualification": "No quantifiers or equality; original atom meanings are retained.",
    }
