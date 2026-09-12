# Argument review

Legitimacy of a Bargain

Provenance: llm_generated. English fidelity: **not assessed**.

## Source

> This bargain is legitimate only if it is voluntary. This bargain is not voluntary. Hence it is not legitimate.

## Claims and translations

| Id | Role / origin | Claim | Exact evidence | Formula |
| --- | --- | --- | --- | --- |
| c1 | premise / explicit | This bargain is legitimate only if it is voluntary. | This bargain is legitimate only if it is voluntary. | (implies L V) |
| c2 | premise / explicit | This bargain is not voluntary. | This bargain is not voluntary. | (not V) |
| c3 | conclusion / explicit | Hence it is not legitimate. | Hence it is not legitimate. | (not L) |

## Argument relations

- c1, c2 supports c3

## Interpretation choices

The following notes are model or fixture annotations, not verified checker results.

Logic: classical_propositional.

Domain: All individuals..

- L, proposition, arity 0: This bargain is legitimate
- V, proposition, arity 0: This bargain is voluntary

- c1: Conditional statement establishing a necessary condition for legitimacy.
- c2: Denial of the necessary condition established in c1.
- c3: Conclusion derived via modus tollens from c1 and c2.
- &#x27;Only if&#x27; was formalized as material implication (L → V) per standard logical convention
- The argument uses propositional logic with two atomic propositions about the bargain&#x27;s properties

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

Reconstruction SHA256: `8876778469b5bc95e25de02e59434ed62cfa87708451f9f6d8f83d84c8053e75`

Formalization SHA256: `3771d184ea0cb3618c2c013c496a2c9919443ae26f865877b26709c62f1d67a5`
