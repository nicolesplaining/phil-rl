"""Original synthetic fixtures, manually specified; NOT model outputs or a benchmark."""

from phil_rl.schema import (
    Artifact,
    Claim,
    Evidence,
    Formalization,
    Reconstruction,
    Relation,
    Symbol,
    Translation,
)


def make(
    title,
    premises,
    conclusion,
    formulas,
    symbols,
    logic="classical_propositional",
    implicit=None,
):
    sentences = premises + [conclusion]
    source = " ".join(sentences)
    claims = [
        Claim(
            id=f"c{i + 1}",
            text=text,
            role="conclusion" if i == len(premises) else "premise",
            origin="explicit",
            evidence=Evidence(quote=text, occurrence=sentences[:i].count(text)),
            interpretation_note="Synthetic wording and reference encoding authored together.",
        )
        for i, text in enumerate(sentences)
    ]
    conclusion_id = claims[-1].id
    premise_ids = [c.id for c in claims[:-1]]
    if implicit:
        claims.append(
            Claim(
                id="bridge",
                text=implicit[0],
                role="premise",
                origin="implicit",
                evidence=None,
                interpretation_note="Proposed missing bridge, not asserted by the source.",
            )
        )
        premise_ids.append("bridge")
        formulas = [*formulas, implicit[1]]
    reconstruction = Reconstruction(
        title=title,
        claims=claims,
        relations=[Relation(premises=premise_ids, conclusion=conclusion_id, kind="supports")]
        if premise_ids
        else [],
        conclusion_id=conclusion_id,
        ambiguities=[],
    )
    formalization = Formalization(
        logic=logic,
        domain_description="Nonempty domain of individuals."
        if logic == "classical_first_order"
        else "Whole propositions; no individual domain is used.",
        symbols=[
            Symbol(name=name, kind=kind, arity=arity, meaning=meaning)
            for name, kind, arity, meaning in symbols
        ],
        translations=[
            Translation(
                claim_id=c.id, formula=f, reason="Unsupported modal semantics." if f is None else ""
            )
            for c, f in zip(claims, formulas, strict=True)
        ],
        interpretation_notes=[
            "Synthetic reference fixture, not an independently assessed translation."
        ],
    )
    return Artifact.create(source, reconstruction, formalization)


def fixtures() -> dict[str, tuple[Artifact, str, str]]:
    """Map names to (reference artifact, expected explicit status, augmented status)."""
    props = [
        ("R", "proposition", 0, "The agent is morally responsible."),
        ("F", "proposition", 0, "The agent acted freely."),
    ]
    result = {}
    result["modus_ponens"] = (
        make(
            "Responsibility and freedom",
            [
                "If the agent is morally responsible, the agent acted freely.",
                "The agent is morally responsible.",
            ],
            "Therefore, the agent acted freely.",
            ["(implies R F)", "R", "F"],
            props,
        ),
        "valid",
        "valid",
    )
    result["affirming_consequent"] = (
        make(
            "Affirming the consequent",
            [
                "If the agent is morally responsible, the agent acted freely.",
                "The agent acted freely.",
            ],
            "Therefore, the agent is morally responsible.",
            ["(implies R F)", "F", "R"],
            props,
        ),
        "invalid",
        "invalid",
    )
    result["missing_bridge"] = (
        make(
            "An unstated bridge",
            ["The agent is morally responsible."],
            "Therefore, the agent acted freely.",
            ["R", "F"],
            props,
            implicit=(
                "If the agent is morally responsible, the agent acted freely.",
                "(implies R F)",
            ),
        ),
        "invalid",
        "valid",
    )
    result["inconsistent"] = (
        make(
            "Contradictory premises",
            ["The agent is morally responsible.", "The agent is not morally responsible."],
            "Therefore, the agent acted freely.",
            ["R", "(not R)", "F"],
            props,
        ),
        "inconsistent_premises",
        "inconsistent_premises",
    )
    result["circular"] = (
        make(
            "A restated conclusion",
            ["The agent acted freely."],
            "Therefore, the agent acted freely.",
            ["F", "F"],
            props,
        ),
        "valid",
        "valid",
    )
    fol_symbols = [
        ("Human", "predicate", 1, "is a human"),
        ("Mortal", "predicate", 1, "is mortal"),
        ("socrates", "constant", 0, "Socrates"),
    ]
    result["syllogism"] = (
        make(
            "Universal instantiation",
            ["Every human is mortal.", "Socrates is human."],
            "Therefore, Socrates is mortal.",
            ["(forall x (implies (Human x) (Mortal x)))", "(Human socrates)", "(Mortal socrates)"],
            fol_symbols,
            "classical_first_order",
        ),
        "valid",
        "valid",
    )
    result["existential_import"] = (
        make(
            "No existential import",
            ["Every human is mortal."],
            "Therefore, a human exists.",
            ["(forall x (implies (Human x) (Mortal x)))", "(exists x (Human x))"],
            fol_symbols,
            "classical_first_order",
        ),
        "invalid",
        "invalid",
    )
    result["scope"] = (
        make(
            "Quantifier scope",
            ["Everyone admires someone."],
            "Therefore, someone is admired by everyone.",
            ["(forall x (exists y (Admires x y)))", "(exists y (forall x (Admires x y)))"],
            [("Admires", "predicate", 2, "The first individual admires the second.")],
            "classical_first_order",
        ),
        "invalid",
        "invalid",
    )
    result["modal"] = (
        make(
            "Modal inference",
            ["Necessarily, every person is self-identical."],
            "Therefore, every person is self-identical.",
            [None, None],
            [],
            "unsupported",
        ),
        "unsupported",
        "unsupported",
    )
    return result
