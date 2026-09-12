"""Stage-specific normalization contracts, without proof-result feedback."""

import re

from phil_rl.logic import parse, validate_formalization

POLICY_VERSION = "0.2"


def explicit_only(reconstruction):
    if any(c.origin == "implicit" for c in reconstruction.claims):
        raise ValueError(
            "This reconstruction stage is explicit-only. Remove proposed implicit claims; "
            "record a genuinely uncertain missing assumption in ambiguities instead. "
            "Do not alter the author's explicit premises or conclusion."
        )
    for claim in reconstruction.claims:
        if claim.role == "reply" and any(
            r.kind == "supports" and claim.id in r.premises for r in reconstruction.relations
        ):
            raise ValueError(
                f"Reply {claim.id} is used as support. Give it the logical role premise "
                "or subconclusion, and retain its reply attribution in interpretation_note."
            )
        if claim.role == "objection" and re.match(
            r"^(?:(?:a|an|the) )?(?:critic|opponent|objector) "
            r"(?:says?|claims?|argues?|contends?)\b",
            claim.text,
            re.IGNORECASE,
        ):
            raise ValueError(
                f"Claim {claim.id} is an objection: text must be its asserted content, "
                "not the reporting frame. Put attribution in interpretation_note and "
                "keep the original evidence. For example, 'A critic says P' has content P."
            )


def normalized_formalization(reconstruction, formalization):
    validate_formalization(reconstruction, formalization)
    if formalization.logic == "unsupported":
        return
    if any(t.formula is None for t in formalization.translations):
        raise ValueError(
            "In this complete-translation stage, every claim needs a formula, including "
            "context and objections. Roles control premise selection, not formalizability. "
            "If actual unsupported semantics prevent translation, choose unsupported "
            "with concrete reasons for the whole artifact."
        )
    active = set(reconstruction.premise_ids()) | {reconstruction.conclusion_id}
    translations = {t.claim_id: t.formula for t in formalization.translations}
    for claim in reconstruction.claims:
        if (
            claim.id in active
            and translations[claim.id] is not None
            and re.search(
                r"\b(usually|typically|probably|necessarily|possibly)\b"
                r"|\b(?:would|could|might) (?:not )?have\b"
                r"|\b(?:knows?|believes?) that\b"
                r"|\bit is (?:possible|necessary) that\b",
                claim.text + " " + (claim.evidence.quote if claim.evidence else ""),
                re.IGNORECASE,
            )
        ):
            raise ValueError(
                f"Claim {claim.id} includes an unsupported qualifier or operator. "
                "Do not erase it or turn it into a universal or material conditional. "
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
