# Argument review

Disjunctive Syllogism on Allocation Properties

Provenance: llm_generated. English fidelity: **not assessed**.

## Source

> Exactly one of these descriptions is true: this allocation is equal, or this allocation is proportional. This allocation is proportional. Therefore this allocation is not equal.

## Claims and translations

| Id | Role / origin | Claim | Exact evidence | Formula |
| --- | --- | --- | --- | --- |
| c1 | premise / explicit | Exactly one of these descriptions is true: this allocation is equal, or this allocation is proportional. | Exactly one of these descriptions is true: this allocation is equal, or this allocation is proportional. | (and (or E P) (not (and E P))) |
| c2 | premise / explicit | This allocation is proportional. | This allocation is proportional. | P |
| c3 | conclusion / explicit | Therefore this allocation is not equal. | Therefore this allocation is not equal. | (not E) |

## Argument relations

- c1, c2 supports c3

## Interpretation choices

The following notes are model or fixture annotations, not verified checker results.

Logic: classical_propositional.

Domain: All atomic propositions..

- E, proposition, arity 0: This allocation is equal
- P, proposition, arity 0: This allocation is proportional

- c1: Exclusive disjunction asserting mutual exclusivity between equality and proportionality
- c2: Affirms one disjunct in the exclusive OR
- c3: Logical consequence derived from the premises
- Exclusive OR is encoded as (E ∨ P) ∧ ¬(E ∧ P) to ensure exactly one disjunct is true
- The conclusion follows by combining the exclusive disjunction with the affirmed disjunct P

## Checks on this encoding

explicit: **valid**. Assumptions: c1, c2.

with_proposed_implicit: **valid**. Assumptions: c1, c2.

Solver results do not assess premise truth, fidelity, or philosophical quality.
Lean statement export alone is not a proof.

## Human review

- [ ] The intended conclusion and speaker are correct.
- [ ] The claims preserve what the evidence says.
- [ ] Every support/attack relation is faithful to the passage.
- [ ] Proposed implicit premises are plausible and remain explicitly labeled.
- [ ] Quantifier scope, negation, and conditional direction are preserved.
- [ ] The selected logic and any abstentions are appropriate.
- [ ] The glossary preserves the intended meanings across claims.

Record disagreements and alternate formalizations before accepting the artifact.

Reconstruction SHA256: `29140c35685b0c41fce8373dd01457d2148d65e9eeb4bb85c51b205444207aa3`

Formalization SHA256: `38b2151e0a0a8387b8cca94fbc6a66255f35bc723ea2983f3972e06eccfe6946`
