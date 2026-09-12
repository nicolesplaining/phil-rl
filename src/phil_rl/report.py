"""Plain Markdown for manual source-to-formula review."""

import html

from phil_rl.schema import Artifact


def cell(text: str) -> str:
    return html.escape(text).replace("|", "&#124;").replace("\n", "<br>").replace("`", "&#96;")


def review(artifact: Artifact, checks: dict, provenance: str) -> str:
    lines = [
        "# Argument review",
        "",
        cell(artifact.reconstruction.title),
        "",
        f"Provenance: {cell(provenance)}. English fidelity: **not assessed**.",
        "",
        "## Source",
        "",
        *("> " + html.escape(line) for line in artifact.source.splitlines()),
        "",
        "## Claims and translations",
        "",
        "| Id | Role / origin | Claim | Exact evidence | Formula |",
        "| --- | --- | --- | --- | --- |",
    ]
    translations = {t.claim_id: t for t in artifact.formalization.translations}
    for claim in artifact.reconstruction.claims:
        translation = translations[claim.id]
        evidence = cell(claim.evidence.quote) if claim.evidence else "Proposed; absent from source"
        formula = (
            cell(translation.formula)
            if translation.formula
            else "Unsupported: " + cell(translation.reason)
        )
        lines.append(
            f"| {claim.id} | {claim.role} / {claim.origin} | {cell(claim.text)} "
            f"| {evidence} | {formula} |"
        )
    lines.extend(["", "## Argument relations", ""])
    for relation in artifact.reconstruction.relations:
        lines.append(f"- {', '.join(relation.premises)} {relation.kind} {relation.conclusion}")
    lines.extend(["", "## Interpretation choices", ""])
    lines.extend(
        [
            f"Logic: {artifact.formalization.logic}.",
            "",
            f"Domain: {cell(artifact.formalization.domain_description)}.",
            "",
        ]
    )
    for symbol in artifact.formalization.symbols:
        lines.append(
            f"- {symbol.name}, {symbol.kind}, arity {symbol.arity}: {cell(symbol.meaning)}"
        )
    lines.append("")
    for claim in artifact.reconstruction.claims:
        if claim.interpretation_note:
            lines.append(f"- {claim.id}: {cell(claim.interpretation_note)}")
    for ambiguity in artifact.reconstruction.ambiguities:
        lines.append(f"- {ambiguity.claim_id}: {cell(ambiguity.issue)}")
        for alternative in ambiguity.alternatives:
            lines.append(f"  - {cell(alternative)}")
    for note in artifact.formalization.interpretation_notes:
        lines.append("- " + cell(note))
    lines.extend(["", "## Checks on this encoding", ""])
    for name, result in checks.items():
        lines.extend(
            [
                f"{name}: **{result['status']}**. Assumptions: "
                + (", ".join(result["included_premise_ids"]) or "none")
                + ".",
                "",
            ]
        )
        if result.get("countermodel"):
            lines.extend(["```text", result["countermodel"], "```", ""])
        for warning in result.get("warnings", []):
            lines.extend(["Warning: " + cell(warning), ""])
    lines.extend(
        [
            "Solver results do not assess premise truth, fidelity, or philosophical quality.",
            "Lean statement export alone is not a proof.",
            "",
            "## Human review",
            "",
            "- [ ] The intended conclusion and speaker are correct.",
            "- [ ] The claims preserve what the evidence says.",
            "- [ ] Every support/attack relation is faithful to the passage.",
            "- [ ] Proposed implicit premises are plausible and remain explicitly labeled.",
            "- [ ] Quantifier scope, negation, and conditional direction are preserved.",
            "- [ ] The selected logic and any abstentions are appropriate.",
            "- [ ] The glossary preserves the intended meanings across claims.",
            "",
            "Record disagreements and alternate formalizations before accepting the artifact.",
            "",
            f"Reconstruction SHA256: `{artifact.reconstruction_sha256}`",
            "",
            f"Formalization SHA256: `{artifact.formalization_sha256}`",
            "",
        ]
    )
    return "\n".join(lines)
