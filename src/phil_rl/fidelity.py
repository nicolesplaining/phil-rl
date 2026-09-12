"""Check formula equivalence under an explicit, separately reviewed glossary mapping.

This cannot establish that the reviewer's English-to-symbol alignment is correct.
It makes that judgment inspectable instead of hiding it in a solver status score.
"""

import z3
from pydantic import Field

from phil_rl.logic import Expr, Z3Compiler, parse, validate_expr
from phil_rl.schema import Artifact, Identifier, Record, fingerprint


class ClaimAlignment(Record):
    reference_ids: list[Identifier] = Field(min_length=1)
    generated_ids: list[Identifier] = Field(min_length=1)


class MeaningReview(Record):
    reference_sha256: str
    generated_sha256: str
    reviewer_kind: str
    symbol_map: dict[Identifier, Identifier]
    glossary_rationale: str = Field(min_length=1)
    claims: list[ClaimAlignment]
    source_meaning_approved: bool
    source_review_notes: str = Field(min_length=1)
    # A narrower generated domain must be an explicitly reviewed unary restriction.
    # Its nonemptiness and constant membership are checked as extra assumptions.
    domain_restriction: Identifier | None = None


def conjunction(values):
    return z3.And(*values)


def translate(expr, mapping, restriction=None, bound=frozenset()):
    op, args = expr.op, expr.args
    if op in {"forall", "exists"}:
        variable = args[0]
        body = translate(args[1], mapping, restriction, bound | {variable.op})
        if restriction:
            guard = Expr(restriction, (variable,))
            body = Expr("implies" if op == "forall" else "and", (guard, body))
        return Expr(op, (variable, body))
    return Expr(
        op if op in bound else mapping.get(op, op),
        tuple(translate(a, mapping, restriction, bound) for a in args),
    )


def assess(reference: Artifact, generated: Artifact, review: MeaningReview, timeout_ms=5000):
    reference = Artifact.model_validate(reference.model_dump())
    generated = Artifact.model_validate(generated.model_dump())
    if review.reference_sha256 != fingerprint(reference) or review.generated_sha256 != fingerprint(
        generated
    ):
        raise ValueError("Review fingerprints do not match the artifacts.")
    if reference.source != generated.source:
        raise ValueError("Cannot compare artifacts with different source passages.")
    if reference.formalization.logic != generated.formalization.logic:
        return {
            "status": "not_equivalent",
            "reason": "Different formal fragments.",
            "fidelity": "not_certified",
        }
    if reference.formalization.logic == "unsupported":
        return {
            "status": "unresolved",
            "reason": "No formulas to compare.",
            "fidelity": "not_certified",
        }
    target = {s.name: s for s in reference.formalization.symbols}
    mapping = review.symbol_map
    if set(mapping) != {s.name for s in generated.formalization.symbols} or len(
        set(mapping.values())
    ) != len(mapping):
        raise ValueError("Glossary alignment must map every generated symbol injectively.")
    for symbol in generated.formalization.symbols:
        counterpart = target.get(mapping[symbol.name])
        if counterpart is None or (counterpart.kind, counterpart.arity) != (
            symbol.kind,
            symbol.arity,
        ):
            raise ValueError("Aligned symbols must have matching kinds and arities.")
    restriction = review.domain_restriction
    if restriction and (
        restriction not in target
        or target[restriction].kind != "predicate"
        or target[restriction].arity != 1
    ):
        raise ValueError("Domain restriction must name a reference unary predicate.")
    compiler = Z3Compiler(reference.formalization)
    ref_formulas = {
        t.claim_id: compiler.compile(parse(t.formula))
        for t in reference.formalization.translations
        if t.formula is not None
    }
    gen_formulas = {}
    for translation in generated.formalization.translations:
        if translation.formula is None:
            continue
        expr = translate(parse(translation.formula), mapping, restriction)
        validate_expr(expr, target, reference.formalization.logic)
        gen_formulas[translation.claim_id] = compiler.compile(expr)
    ref_claims = {c.id: c for c in reference.reconstruction.claims if c.origin == "explicit"}
    gen_claims = {c.id: c for c in generated.reconstruction.claims if c.origin == "explicit"}
    for label, expected in [("reference_ids", ref_claims), ("generated_ids", gen_claims)]:
        selected = [key for group in review.claims for key in getattr(group, label)]
        if len(selected) != len(set(selected)) or set(selected) != set(expected):
            raise ValueError("Claim alignment must cover every explicit claim exactly once.")

    def equivalent(left, right, assumptions=()):
        solver = z3.Solver()
        solver.set(timeout=timeout_ms)
        solver.add(*assumptions, left != right)
        result = solver.check()
        return (
            "equivalent"
            if result == z3.unsat
            else "not_equivalent"
            if result == z3.sat
            else "unresolved"
        )

    domain_assumptions = []
    if restriction:
        variable = Expr("fidelityDomainMember")
        domain_assumptions.append(
            compiler.compile(Expr("exists", (variable, Expr(restriction, (variable,)))))
        )
        for symbol in generated.formalization.symbols:
            if symbol.kind == "constant":
                domain_assumptions.append(
                    compiler.compile(Expr(restriction, (Expr(mapping[symbol.name]),)))
                )

    groups = []
    for group in review.claims:
        refs = [ref_claims[k] for k in group.reference_ids]
        gens = [gen_claims[k] for k in group.generated_ids]
        roles_match = len({c.role for c in refs + gens}) == 1

        # A group may merge/split conjuncts of the same role, but not move evidence.
        def coverage(claims):
            covered = set()
            for claim in claims:
                start, end = claim.evidence.locate(reference.source)
                covered.update(i for i in range(start, end) if not reference.source[i].isspace())
            return covered

        evidence_match = coverage(refs) == coverage(gens)
        formulas_exist = all(c.id in ref_formulas for c in refs) and all(
            c.id in gen_formulas for c in gens
        )
        status = (
            equivalent(
                conjunction([ref_formulas[c.id] for c in refs]),
                conjunction([gen_formulas[c.id] for c in gens]),
                domain_assumptions,
            )
            if formulas_exist
            else "unresolved"
        )
        groups.append(
            {
                **group.model_dump(),
                "roles_match": roles_match,
                "evidence_match": evidence_match,
                "formula_comparison": status,
            }
        )
    ref_premises = reference.reconstruction.premise_ids()
    gen_premises = generated.reconstruction.premise_ids()
    if all(k in gen_formulas for k in gen_premises):
        premise_status = equivalent(
            conjunction([ref_formulas[k] for k in ref_premises]),
            conjunction([gen_formulas[k] for k in gen_premises] + domain_assumptions),
        )
    else:
        premise_status = "unresolved"
    good = (
        review.source_meaning_approved
        and premise_status == "equivalent"
        and all(
            row["roles_match"]
            and row["evidence_match"]
            and row["formula_comparison"] == "equivalent"
            for row in groups
        )
    )
    return {
        "status": "passed_under_reviewed_alignment" if good else "not_passed",
        "fidelity": "conditional_on_reviewer_alignment",
        "reviewer_kind": review.reviewer_kind,
        "active_premises": premise_status,
        "claim_groups": groups,
        "implicit_claims": [
            c.id for c in generated.reconstruction.claims if c.origin == "implicit"
        ],
        "qualification": "Formal correspondence depends on the reviewer's English interpretation.",
    }
