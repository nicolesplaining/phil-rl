# Working-version evaluation

The third frozen run meets the numerical acceptance gate for the bounded first
stage. It does not establish reliability on arbitrary philosophy or replace source
review. The evaluated code is `b83158a1901ff51a483228d79dca06fd141325e8`, with prompt
version 0.6 and policy version 0.2. V1 and V2 had already become development sets.

| Check | Result |
| --- | --- |
| Completed outcomes | 40/40, no request or schema-exhaustion failures |
| Supported cases passing reviewed formula and active-premise equivalence | 31/32, 96.875% |
| Unsupported-logic controls | 5/5 abstentions, with their operators retained |
| Non-argument controls | 2/2 correctly identified |
| Scope-ambiguity control | 1/1 flagged for review |
| Propositional proofs checked by Lean | 15/15 |
| Additional Lean statement definitions checked | 17/17, not proofs |

The supported non-pass is u15. The model called a circular restatement a non-argument.
The source uses 'So' to present an inference; lack of new information does not make
it cease to be an argument. This remains a known false abstention and counts against
the denominator. The model was not tuned on this final run's failure.

The fidelity score is conditional on agent-authored references and glossary review.
The evaluated Qwen model received only source text, never the references, expected
verdicts or reviewer mappings. Formula comparisons cover conditional direction,
negation, quantifier scope, evidence coverage, claim roles and active assumptions.
In u08, a single neither/nor premise was split into two conjuncts; the review records
that alignment explicitly rather than requiring a literal string match.

These are lexically new synthetic passages, not a randomly sampled or expert-labeled
corpus. Many logical structures repeat across the three sets. The result supports an
engineering acceptance decision, not a population-level accuracy claim or evidence
that RL improves philosophy.

Model commentary remains unreliable. u27 includes a poor note about validity, and
u38 overstates one scope alternative as involving unique distinct positions. The
selected formulas do not contain those extra restrictions. u38 passes the
review-signal category, not an assessment that its alternative wording is correct.
Interpretation notes are not verified philosophical claims and should not be used
as quality rewards.

Lean checked proofs only for supported, consistent propositional arguments. The ten
first-order cases and the ambiguous first-order example have checked statement
definitions, not Lean proofs. Z3 handles their logical diagnostics; finite model
search can refute entailment but cannot certify validity by failing to find a model.

The historical v2 counterfactual q34 is a cautionary example: Lean accepts a proof of
its incorrectly strengthened encoding. That archived proof is genuine, but it does
not verify the English argument. Current modal guards reject that translation.

## Reproduce the saved checks

```bash
uv sync --locked --python 3.12
uv run phil audit experiments/heldout-v3 \
  --decisions experiments/reviews/v3-decisions.json --out outputs/replayed-audit
uv run phil verify-run experiments/heldout-v3 --out outputs/replayed-lean
uv run pytest -q
```

Install the pinned Lean toolchain before the second command. The CI Lean job also
rechecks every final exported proof and definition. Archives include failed and
abstained runs, raw responses, source/prompt/schema hashes and file manifests.
`runtime.json` records model, revision evidence and serving configuration. Repeating
inference requires the model server; replaying saved checks does not.

The user-facing README remains unchanged. Usage and limitations are in `docs/`.
RL training, paper generation and philosophical-quality scoring remain later work.
