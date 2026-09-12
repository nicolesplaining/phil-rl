# Argument review

Exclusive Disjunction Argument

Provenance: llm_generated. English fidelity: **not assessed**.

## Source

> Exactly one of these claims is true: this decision is final, or this decision is revisable. This decision is final. Hence this decision is not revisable.

## Claims and translations

| Id | Role / origin | Claim | Exact evidence | Formula |
| --- | --- | --- | --- | --- |
| c1 | premise / explicit | Exactly one of these claims is true: this decision is final, or this decision is revisable. | Exactly one of these claims is true: this decision is final, or this decision is revisable. | (and (or F R) (not (and F R))) |
| c2 | premise / explicit | This decision is final. | This decision is final. | F |
| c3 | conclusion / explicit | This decision is not revisable. | Hence this decision is not revisable. | (not R) |

## Argument relations

- c1, c2 supports c3

## Interpretation choices

The following notes are model or fixture annotations, not verified checker results.

Logic: classical_propositional.

Domain: All individuals..

- F, proposition, arity 0: This decision is final
- R, proposition, arity 0: This decision is revisable


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

Reconstruction SHA256: `b52b273032a55c869dfb2557f0cd94d0242fcc12087e117dce466300462d50be`

Formalization SHA256: `6b484ddba145e46283d729d68454b28d2b2a123a0156c9c16e36c31d5f180eda`
