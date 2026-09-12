# First frozen evaluation

This run failed the working-version acceptance gate and is now development data.
The source-only evaluation used commit `76c99b1035ed0aec1a8d458cb091e585eadc46bc`,
prompt version 0.4, Qwen3-32B with reasoning, and four request workers on GPU 1.
All 40 cases completed; 38 produced artifacts and two failed reconstruction.

The strict source/glossary review passed 26 of 32 supported cases and 5 of 8 other
cases. The references and reviews are agent-authored, not independent human labels.
Formula equivalence is conditional on that English glossary review.

The six supported non-passes include different problems:

- h02 has a reference problem: the source permits a generic conditional, but the
  reference uses an instance-level one. It remains in the denominator as unresolved.
- h08, h10 and h18 do not fit the strict renaming protocol because of an unused
  compound declaration or negative atoms. This is not proof of semantic error.
- h29 silently imposes a nonempty people domain, strengthening the explicit premises.
- h30 replaces identity with an uninterpreted relation and loses substitution.

Among the other cases, h37 strengthens 'usually' to a universal rule. Its own warning
acknowledges the change, but that does not make the resulting valid encoding faithful.
The two non-argument failures omitted optional status fields on all retries. The
quantifier-scope ambiguity in h38 is correctly recorded and needs review.

The revisions use required outcome fields, explicit-only reconstruction, unrestricted
individual domains, explicit logical negation, and structural normalization checks.
A targeted ten-case development run recovered the expected statuses, and a further
negation test confirmed explicit operators. These reruns are development evidence,
not a second held-out result. A fresh 40-case v2 suite was specified before inference.

Raw outputs, unsuccessful attempts, traces and checks are under `heldout-v1/`.
The checksum manifest identifies the saved files. Review decisions and reproducible
formula comparisons are under `reviews/`. No original artifact was corrected in place.
