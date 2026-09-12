"""The model proposes interpretations; these schemas enforce structural contracts."""

import hashlib
import json
import re
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Identifier = Annotated[str, Field(pattern=r"^[A-Za-z][A-Za-z0-9_]{0,63}$")]
Text = Annotated[str, Field(min_length=1, max_length=20000)]


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Evidence(Record):
    quote: Text
    occurrence: int = Field(ge=0, description="Zero-based occurrence of this exact quote.")

    def locate(self, source: str) -> tuple[int, int]:
        matches = list(re.finditer(re.escape(self.quote), source))
        if self.occurrence >= len(matches):
            raise ValueError("Evidence quote/occurrence is absent from the source.")
        match = matches[self.occurrence]
        return match.start(), match.end()


class Claim(Record):
    id: Identifier
    text: Text
    role: Literal["premise", "subconclusion", "conclusion", "objection", "reply", "context"]
    origin: Literal["explicit", "implicit"]
    evidence: Evidence | None
    interpretation_note: str = Field(max_length=4000)

    @model_validator(mode="after")
    def evidence_policy(self):
        if self.origin == "explicit" and self.evidence is None:
            raise ValueError("Explicit claims require exact source evidence.")
        if self.origin == "implicit" and (
            self.evidence is not None or not self.interpretation_note
        ):
            raise ValueError(
                "Implicit claims need an explanation and must not claim source evidence."
            )
        if self.origin == "implicit" and self.role != "premise":
            raise ValueError("Only proposed premises may be implicit in this prototype.")
        return self


class Relation(Record):
    premises: list[Identifier] = Field(min_length=1, max_length=64)
    conclusion: Identifier
    kind: Literal["supports", "attacks"]


class Ambiguity(Record):
    claim_id: Identifier
    issue: Text
    alternatives: list[Text] = Field(min_length=2, max_length=8)


class Reconstruction(Record):
    title: Text
    claims: list[Claim] = Field(min_length=1, max_length=64)
    relations: list[Relation] = Field(max_length=128)
    conclusion_id: Identifier
    ambiguities: list[Ambiguity] = Field(max_length=64)

    @model_validator(mode="after")
    def graph_policy(self):
        claims = {c.id: c for c in self.claims}
        if len(claims) != len(self.claims):
            raise ValueError("Claim ids must be unique.")
        if self.conclusion_id not in claims or claims[self.conclusion_id].role != "conclusion":
            raise ValueError("conclusion_id must reference an explicit conclusion.")
        for a in self.ambiguities:
            if a.claim_id not in claims:
                raise ValueError("Ambiguity references an unknown claim.")
        edges: dict[str, set[str]] = {key: set() for key in claims}
        for relation in self.relations:
            if relation.conclusion not in claims or any(p not in claims for p in relation.premises):
                raise ValueError("Relation references an unknown claim.")
            if len(set(relation.premises)) != len(relation.premises):
                raise ValueError("Duplicate premises in a relation.")
            if relation.conclusion in relation.premises:
                raise ValueError("A claim cannot directly support or attack itself.")
            if relation.kind == "supports":
                for premise in relation.premises:
                    edges[premise].add(relation.conclusion)
        visiting, visited = set(), set()

        def visit(node):
            if node in visiting:
                raise ValueError("Support graph must be acyclic; describe circularity in notes.")
            if node in visited:
                return
            visiting.add(node)
            for target in edges[node]:
                visit(target)
            visiting.remove(node)
            visited.add(node)

        for node in edges:
            visit(node)
        return self

    def validate_source(self, source: str) -> None:
        for claim in self.claims:
            if claim.evidence:
                claim.evidence.locate(source)

    def premise_ids(self, include_implicit: bool = False) -> list[str]:
        """Only premises on a support path to the selected conclusion are assumptions.

        Intermediate conclusions must follow from their leaves; they are never axioms.
        Objections and contextual statements cannot become assumptions by accident.
        """
        reachable = {self.conclusion_id}
        while True:
            expanded = reachable | {
                p
                for r in self.relations
                if r.kind == "supports" and r.conclusion in reachable
                for p in r.premises
            }
            if expanded == reachable:
                break
            reachable = expanded
        return [
            c.id
            for c in self.claims
            if c.id in reachable
            and c.role == "premise"
            and (include_implicit or c.origin == "explicit")
        ]


class Symbol(Record):
    name: Identifier
    kind: Literal["proposition", "predicate", "constant"]
    arity: int = Field(ge=0, le=8)
    meaning: Text

    @model_validator(mode="after")
    def arity_policy(self):
        if self.kind == "predicate" and self.arity == 0:
            raise ValueError(
                "Predicates take at least one argument; use proposition for arity zero."
            )
        if self.kind != "predicate" and self.arity != 0:
            raise ValueError("Only predicates have nonzero arity.")
        if self.name in {
            "and",
            "or",
            "not",
            "implies",
            "iff",
            "forall",
            "exists",
            "eq",
            "true",
            "false",
        }:
            raise ValueError("Symbol name is a reserved logical operator.")
        return self


class Translation(Record):
    claim_id: Identifier
    formula: str | None = Field(max_length=20000)
    reason: str = Field(max_length=4000)

    @model_validator(mode="after")
    def missing_formula(self):
        if self.formula is None and not self.reason:
            raise ValueError("Unformalized claims require a reason.")
        return self


class Formalization(Record):
    logic: Literal["classical_propositional", "classical_first_order", "unsupported"]
    domain_description: Text
    symbols: list[Symbol] = Field(max_length=128)
    translations: list[Translation] = Field(min_length=1, max_length=64)
    interpretation_notes: list[Text] = Field(max_length=64)


def fingerprint(value: object) -> str:
    if isinstance(value, BaseModel):
        value = value.model_dump(mode="json")
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()


class Artifact(Record):
    schema_version: Literal["0.1"] = "0.1"
    source: Text
    source_sha256: str
    reconstruction: Reconstruction
    reconstruction_sha256: str
    formalization: Formalization
    formalization_sha256: str

    @model_validator(mode="after")
    def integrity(self):
        for name in ("source", "reconstruction", "formalization"):
            if fingerprint(getattr(self, name)) != getattr(self, name + "_sha256"):
                raise ValueError(f"{name} fingerprint mismatch.")
        self.reconstruction.validate_source(self.source)
        from phil_rl.logic import validate_formalization

        validate_formalization(self.reconstruction, self.formalization)
        return self

    @classmethod
    def create(cls, source: str, reconstruction: Reconstruction, formalization: Formalization):
        return cls(
            source=source,
            source_sha256=fingerprint(source),
            reconstruction=reconstruction,
            reconstruction_sha256=fingerprint(reconstruction),
            formalization=formalization,
            formalization_sha256=fingerprint(formalization),
        )
