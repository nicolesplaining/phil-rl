# Initial experiment

The prototype runs English argument reconstruction and formalization with Qwen3-32B,
then checks the fixed encoding with Z3. A generated propositional argument also
passed Lean's kernel check. This is an implementation experiment on a small
development set, not a benchmark of philosophical ability.

## Setup

- Date: September 13, 2026, Asia/Shanghai. Trace timestamps use UTC.
- Model: `Qwen/Qwen3-32B`, revision `9216db5781bf21249d130ec9da846c4624c16137`.
- Runtime: vLLM 0.19.1, PyTorch 2.10.0, bfloat16, eager execution.
- Hardware: one NVIDIA H100 80GB, physical GPU 1. GPU 0 belonged to another project.
- Context: 16,384 tokens. One scheduled sequence. GPU memory fraction: 0.90.
- Sampling: temperature 0, seed 0, thinking disabled, 8,192 maximum output tokens.
  Model generation defaults supplied top-k 20 and top-p 0.95. Greedy sampling was requested.
- Two separate model stages, JSON-schema constrained decoding, at most two repair
  attempts after the initial response. Repairs received structural errors only.
- Verifiers: Z3 4.16.0 and Lean 4.19.0. No mathlib, arbitrary model code, or extra axioms.

Public weights downloaded without authentication. No Hugging Face token was needed.

## Development runs

Each model invocation received only the English source. Reference formulas and
expected statuses were withheld. The nine reference arguments were manually
specified alongside their original synthetic wording. They are not independent
expert annotations or representative samples of published philosophy.

| Run | Completed artifacts | Explicit status matches | Augmented status matches |
| --- | --- | --- | --- |
| Prompt 0.1 | 9/9 | 5/9 | 3/9 |
| Prompt 0.2 | 8/9 | 6/9 | 6/9 |
| Targeted modal retry with better evidence errors | 1/1 | 1/1 | 1/1 |

The second run used development feedback to clarify preservation of circularity,
contradictions, and modal language. It also put the JSON schema in the model's
context, in addition to using it for constrained decoding. Several changes were
made together, so the results do not isolate any one intervention's effect.

The targeted retry changed the exact-quote validation error to identify the claim,
quote, and case-sensitive matching requirement. It is a separate run on one known
failure, not a fresh nine-case evaluation. Its reconstruction took two attempts and
formalization took three. The final result correctly abstained on modal semantics.

Status matches include invalidity, inconsistency and abstention. They do not mean
that the model generated that many valid arguments, and they do not measure semantic
equivalence or philosophical quality. Augmented checks also depend on which optional
implicit premises the model proposes; matching that reference is not always desirable.

## Observed failures

1. In the first run, affirming the consequent acquired a proposed converse premise.
   Z3 kept the explicit argument invalid and found the augmented version valid.
   The model's interpretation notes incorrectly claimed the augmented version was
   invalid. Those notes are not checker results.
2. Both runs sometimes treated ordinary responsibility/free-action propositions as
   requiring unavailable semantics. The missing-bridge case should be expressible
   as two unrelated propositions, with an invalid explicit inference.
3. Both runs abstained on contradictory premises instead of preserving `P` and
   `not P`. An early second-run response even encoded negation as an unrelated
   proposition. This demonstrates why successful JSON validation is insufficient.
4. The first run mislabeled a repeated premise as a conclusion, leaving no active
   assumptions. The second run preserved the explicit premise and the checker
   warned that its formula repeats the conclusion.
5. The first modal translation dropped "necessarily" and produced a valid FOL
   inference. Its notes explicitly admitted the omission. A theorem checker could
   accept that encoding without detecting the loss of English meaning.
6. The second modal reconstruction capitalized a quote that was lowercase in the
   source. Three attempts repeated the mismatch. More specific structural feedback
   fixed this in the targeted retry without weakening the evidence requirement.

A longer, original objection-and-reply passage is preserved in `qwen32b-objection/`.
The model recovered seven claims and abstained on the counterfactual/modal content.
However, it labeled the objector's claim as context and omitted the inability-to-do-
otherwise claim from the active support premises. The reconstruction needs review.

## Verification and files

The code test suite passed 56 tests before archiving these runs, including eight
Lean integration tests. The nine manually specified solver fixtures all returned
their expected explicit and augmented statuses.
The final suite passed 75 tests after adding 19 replay checks for archived artifacts.

`qwen32b-refined-proof.lean` was generated deterministically from the refined live
modus-ponens formalization and checked with Lean 4.19.0. Its reported axioms were
`propext`, `Classical.choice`, and `Quot.sound`; no `sorryAx` was present. This proves
the encoded implication and says nothing about the truth of its premises.

Each run directory contains the original arguments, translations, exact evidence,
full successful-stage responses and repair traces, checker outputs, and review
documents. `summary.json` retains generation failures in the denominator. The failed
modal reconstruction has `failure.json` rather than a fabricated argument artifact.

Setup and commands are in [the usage guide](../../docs/usage.md). Start with the
review documents and compare them to the source before accepting any formalization.
The next research step is an independently annotated fidelity set and evaluation of
argument roles, scope, negation, implicit-premise precision, and abstention. These
results do not justify using compilation success as a translation-quality reward.
