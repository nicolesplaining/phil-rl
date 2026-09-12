"""Stage-specific normalization contracts, without proof-result feedback."""

import re

from phil_rl.logic import parse, validate_formalization

POLICY_VERSION = "0.1"


def explicit_only(reconstruction):
    if any(c.origin == "implicit" for c in reconstruction.claims):
        raise ValueError(
            "This reconstruction stage is explicit-only. Remove proposed implicit claims; "
            "record a genuinely uncertain missing assumption in ambiguities instead. "
            "Do not alter the author's explicit premises or conclusion."
        )


def normalized_formalization(reconstruction, formalization):
    validate_formalization(reconstruction, formalization)
    if formalization.logic == "unsupported":
        return
    active = set(reconstruction.premise_ids()) | {reconstruction.conclusion_id}
    translations = {t.claim_id: t.formula for t in formalization.translations}
    for claim in reconstruction.claims:
        if (
            claim.id in active
            and translations[claim.id] is not None
            and re.search(
                r"\b(usually|typically|probably)\b",
                claim.text + " " + (claim.evidence.quote if claim.evidence else ""),
                re.IGNORECASE,
            )
        ):
            raise ValueError(
                f"Claim {claim.id} includes a defeasible or probabilistic qualifier. "
                "Do not translate it as a strict universal or material conditional. "
                "This fragment requires abstention: use a null formula with a reason."
            )
    if (
        formalization.logic == "classical_first_order"
        and formalization.domain_description != "All individuals."
    ):
        raise ValueError(
            "Use domain_description 'All individuals.'. Encode noun restrictions with unary "
            "predicates inside quantifiers, not by restricting the domain. A nonempty "
            "individual domain does not imply any person, act, belief, or judge exists."
        )
    mentioned = set()

    def visit(expr):
        mentioned.add(expr.op)
        for arg in expr.args:
            visit(arg)

    for translation in formalization.translations:
        if translation.formula:
            visit(parse(translation.formula))
    for symbol in formalization.symbols:
        if symbol.kind == "proposition" and re.search(
            r"\b(?:is|are|was|were|does|do|did) not\b|^not\b", symbol.meaning, re.IGNORECASE
        ):
            raise ValueError(
                f"Symbol {symbol.name} embeds explicit negation in its English meaning. "
                "Use a positive atom and (not ...) in each corresponding formula. "
                "Do not simply delete 'not' from the meaning: preserve every frozen claim."
            )
        if symbol.name not in mentioned:
            raise ValueError(f"Unused glossary symbol {symbol.name}. Remove only its declaration.")
        if symbol.kind == "predicate" and re.fullmatch(
            r"(?:identity|equality)(?: relation)?\.?", symbol.meaning.strip(), re.IGNORECASE
        ):
            raise ValueError(
                "Individual identity uses built-in (eq a b), with no declared equality "
                "predicate. An uninterpreted relation does not provide substitution."
            )
