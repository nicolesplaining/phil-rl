"""Deterministic source units: the model selects evidence, it does not retype it."""

import re
from typing import Literal

from pydantic import Field, model_validator

from phil_rl.schema import (
    Ambiguity,
    Claim,
    Evidence,
    Identifier,
    Reconstruction,
    Record,
    Relation,
    Text,
)


class SourceUnit(Record):
    id: Identifier
    start: int = Field(ge=0)
    end: int = Field(ge=1)
    text: Text


def source_units(source: str) -> list[SourceUnit]:
    """Split at sentence/line boundaries without changing any source characters.

    This is evidence indexing, not a claim that each unit is a logical sentence.
    Abbreviations may yield extra units; a claim can cite adjacent units together.
    Decimal points and sentence-internal semicolons are kept.
    """
    boundaries = [0]
    for match in re.finditer(r"[.!?]+[\"'”’)]*(?=\s|$)|\n+", source):
        boundaries.append(match.end())
    boundaries.append(len(source))
    units = []
    for start, end in zip(boundaries, boundaries[1:], strict=False):
        while start < end and source[start].isspace():
            start += 1
        while end > start and source[end - 1].isspace():
            end -= 1
        if start < end:
            units.append(
                SourceUnit(id=f"s{len(units) + 1}", start=start, end=end, text=source[start:end])
            )
    if len(units) > 256:
        raise ValueError("Passage has more than 256 source units; select a shorter argument.")
    return units


class GroundedClaim(Record):
    id: Identifier
    text: Text = Field(
        description="Asserted content; put an objector's attribution in interpretation_note."
    )
    role: Literal["premise", "subconclusion", "conclusion", "objection", "reply", "context"]
    origin: Literal["explicit", "implicit"]
    evidence_ids: list[Identifier] = Field(max_length=32)
    interpretation_note: str = Field(max_length=4000)


class GroundedReconstruction(Record):
    status: Literal["argument", "no_argument"]
    reason: str = Field(max_length=4000)
    title: Text
    claims: list[GroundedClaim] = Field(max_length=64)
    relations: list[Relation] = Field(max_length=128)
    conclusion_id: Identifier | None
    ambiguities: list[Ambiguity] = Field(max_length=64)

    @model_validator(mode="after")
    def outcome_policy(self):
        if self.status == "argument" and (not self.claims or self.conclusion_id is None):
            raise ValueError("An argument requires claims and a conclusion id.")
        if self.status == "no_argument" and (
            self.claims
            or self.relations
            or self.ambiguities
            or self.conclusion_id is not None
            or not self.reason.strip()
        ):
            raise ValueError(
                "No-argument outcomes need a reason, empty claims/relations/ambiguities, "
                "and null conclusion."
            )
        return self

    def materialize(self, source: str, units: list[SourceUnit]) -> Reconstruction:
        if self.status != "argument":
            raise ValueError("Cannot materialize a no-argument outcome.")
        positions = {unit.id: i for i, unit in enumerate(units)}
        cited = {
            key for claim in self.claims if claim.origin == "explicit" for key in claim.evidence_ids
        }
        missing = set(positions) - cited
        if missing:
            raise ValueError(
                f"Source units {', '.join(sorted(missing))} have no claim. Retain background "
                "as context instead of dropping it. Each citation must support the claim "
                "it accompanies; do not attach omitted text to an unrelated claim."
            )
        claims = []
        for draft in self.claims:
            if draft.origin == "implicit":
                if draft.evidence_ids:
                    raise ValueError(f"Implicit claim {draft.id} must not cite explicit evidence.")
                evidence = None
            else:
                if not draft.evidence_ids or any(
                    key not in positions for key in draft.evidence_ids
                ):
                    raise ValueError(
                        f"Explicit claim {draft.id} must cite existing source unit ids."
                    )
                indices = [positions[key] for key in draft.evidence_ids]
                if indices != list(range(indices[0], indices[-1] + 1)):
                    raise ValueError(f"Evidence units for {draft.id} must be ordered and adjacent.")
                first, last = units[indices[0]], units[indices[-1]]
                quote = source[first.start : last.end]
                matches = list(re.finditer(re.escape(quote), source))
                occurrence = next(
                    (i for i, match in enumerate(matches) if match.start() == first.start), None
                )
                if occurrence is None:
                    raise ValueError(
                        f"Evidence for {draft.id} overlaps an earlier identical quote. "
                        "Use a single source unit or a wider unambiguous evidence span."
                    )
                evidence = Evidence(quote=quote, occurrence=occurrence)
            claims.append(
                Claim(
                    id=draft.id,
                    text=draft.text,
                    role=draft.role,
                    origin=draft.origin,
                    evidence=evidence,
                    interpretation_note=draft.interpretation_note,
                )
            )
        reconstruction = Reconstruction(
            title=self.title,
            claims=claims,
            relations=self.relations,
            conclusion_id=self.conclusion_id,
            ambiguities=self.ambiguities,
        )
        reconstruction.validate_source(source)
        return reconstruction
