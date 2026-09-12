# Usage

This first prototype takes a short English argument through two LLM calls:

1. Reconstruct claims and their support/attack relations, with exact source evidence.
2. Translate those frozen claims into propositional or function-free first-order logic.

It then checks the fixed encoding with Z3 and exports a Lean statement. Small valid
propositional arguments can also produce deterministic proofs for Lean to check.
It does not train a model, judge philosophical quality, or certify English fidelity.

## Local quickstart

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```bash
uv sync --locked --python 3.12
uv run phil demo --out outputs/demo
uv run pytest -q
```

The demo uses nine manually specified synthetic fixtures. It checks modus ponens,
affirming the consequent, a missing bridge, inconsistent premises, a repeated
conclusion, universal instantiation, existential import, quantifier scope, and modal
abstention. These are engineering tests, not measured LLM performance.

## Run a model

On the GPU machine, clone main and launch the server:

```bash
git clone https://github.com/nicolesplaining/phil-rl.git
cd phil-rl
bash scripts/serve.sh
```

The shared-node default is Qwen3-32B in bfloat16 on physical GPU 1, with tensor
parallelism set to one. GPU 0 is reserved for another project. The server binds to
loopback port 8011. From your local machine, open an SSH tunnel:

```bash
ssh -N -L 8000:127.0.0.1:8011 ubuntu@YOUR_GPU_HOST
```

Then run:

```bash
uv run phil run examples/responsibility.txt --out outputs/responsibility
uv run phil run examples/missing-premise.txt --out outputs/missing-premise
uv run phil check outputs/missing-premise/argument.json
uv run phil check outputs/missing-premise/argument.json --include-implicit
```

`PHIL_BASE_URL`, `PHIL_MODEL`, and `PHIL_API_KEY` configure another chat-completions
endpoint. The default is `http://127.0.0.1:8000/v1`, with no API key. Set secrets in
the environment; do not put tokens in scripts or commit them. Public Qwen weights do
not require a Hugging Face token. `HF_TOKEN`, if needed for downloads, belongs only
in the server environment. It is distinct from an inference endpoint's API key.

Qwen reasoning is enabled by the server by default. `--no-thinking` disables it
for a comparison run. The client otherwise sends no model-specific template options.
The older `--no-qwen-template` option is retained for compatibility. Use
`--no-structured` for endpoints without JSON-schema constrained generation. The
fallback still validates JSON and claim/evidence contracts. Retries receive only
structural errors, never solver feedback. Run `uv run phil run --help` for limits.

Successful argument directories contain:

- `argument.json`: the source, reconstruction, glossary, formalization, and hashes.
- `trace.json`: model settings, prompt hashes, responses, retries, and source offsets.
- `checks.json`: separate explicit-premise and proposed-implicit-premise checks.
- `Statement.lean`: a definition of the argument's statement, when supported.
- `review.md`: source evidence, claims, formulas, interpretation notes and a human review checklist.

Existing output paths are refused. Source offsets count Unicode code points and use
half-open intervals. Generated artifacts can contain the input text verbatim and
stay under git-ignored `outputs/` by default.

Reconstruction selects source-unit identifiers. The program resolves these to exact
quotes, so the model cannot introduce a quotation typo. This does not establish that
its paraphrase preserves the quote's meaning. Non-argument inputs produce a
`no_argument` outcome and no Lean file. Failed model calls retain `failure.json` and
a trace, including the frozen reconstruction when formalization failed. Transient
network retries are bounded separately from structural retries.

Complete reconstruction requires evidence coverage of every source unit, including
background. Coverage is only a structural check; it does not prove that each claim
faithfully interprets its citation. Attribution stays in the role and notes, while an
objection's claim text states the opponent's asserted content.

Ground first-order formulas without quantifiers or equality are deterministically
abbreviated as propositions. The trace retains the original formulas, predicate and
argument meanings, and the inverse substitution map. Exact structural round-trip
checks prevent this normalization from changing a formula. Quantified and equality
formulas are not abstracted this way.

## Lean

Install [Lean through elan](https://lean-lang.org/install/). `lean-toolchain` pins
Lean 4.19.0. No mathlib dependency is needed.

```bash
uv run phil lean outputs/demo/modus_ponens/argument.json \
  --out outputs/proof.lean --prove --check
uv run phil lean outputs/demo/syllogism/argument.json \
  --out outputs/fol-statement.lean --check
```

The first command generates and checks a proof. The second only checks that the
statement is well typed. `proof_checked` remains false for a definition, even when
Lean accepts the file. First-order proof search is not implemented. Automatic
propositional proofs use bounded case splitting, with a limit of eight symbols.
The system rejects inconsistent premises before proof generation and checks for
`sorryAx`. The ordinary Lean classical axioms are permitted.

## Interpretation contracts

- Explicit claims require verbatim source evidence. This tests provenance, not
  whether the normalized claim faithfully paraphrases that evidence.
- New reconstruction runs extract explicit claims only. They may flag missing
  assumptions for review but cannot insert them into the graph. Historical and
  manual artifacts can contain proposed implicit premises; checks exclude those
  by default and label the augmented argument when included.
- The formalizer must translate each reconstructed claim exactly once. It cannot
  add premises or remove the conclusion. Hashes detect accidental changes; they
  are not cryptographic attestations against an adversary who can rewrite hashes.
- Only premise-role claims on a support path to the main conclusion become
  assumptions. Objections, background claims, and intermediate conclusions do not.
  Support edges record a proposed reading, not a checked inference.
- The language supports classical propositional logic and single-sorted FOL over
  a nonempty domain, with constants, relations, equality, and quantifiers. There
  are no unique-name or finite-domain assumptions.
- New first-order runs use an unrestricted individual domain and explicit noun
  predicates. This avoids assuming a class exists merely by quantifying over it.
  Bounded model search can supply a finite counterexample, but failure to find one
  never establishes validity. Explicit negation uses operators, not negative atoms.
- Modal, epistemic, deontic, probabilistic, and counterfactual reasoning require
  additional semantics. The prompt requests abstention where these are essential.
  Detecting an incorrect decision to flatten such language still requires review.
- Outcomes are `valid`, `invalid`, `inconsistent_premises`, `unsupported`, or
  `unknown`. An invalid encoding includes a Z3 countermodel. Solver timeouts do not
  count as validity or invalidity.

`uv run phil schema reconstruction` and `uv run phil schema formalization` show the
model schemas. Formula syntax uses prefix expressions, for example:

```text
(implies Responsible Free)
(forall x (implies (Human x) (Mortal x)))
(exists y (forall x (Admires x y)))
```

Model-generated code never executes. A parser validates formula names, arities,
variable scopes and resource limits before compiling to Z3 and Lean.

## Research scope

The first experiment should measure source fidelity, recovered support relations,
implicit-premise precision, scope preservation and appropriate abstention, with
human review. Logical validity is a separate diagnostic. Increasing the percentage
of valid outputs would be a bad objective for faithful translation of invalid inputs.

The included passages are original synthetic examples. They are small enough for
manual inspection and are not a representative philosophy corpus. `objection.txt`
is a harder prose example without a reference encoding.

Run the model on all nine synthetic passages with:

```bash
uv run phil evaluate --out outputs/baseline
```

Use `--cases modus_ponens missing_bridge scope modal` for a smaller run. Each case
uses only the English source; reference formulas and expected statuses are withheld
from the model. The summary records generation failures, retries and agreement
with the reference's solver status. Matching status alone does not establish
semantic equivalence. Review each `review.md` before drawing conclusions about
translation quality. Evaluation exits nonzero on generation failures; semantic
disagreements remain in the report rather than triggering proof-driven repairs.

The serving setup follows the [Qwen3 model card](https://huggingface.co/Qwen/Qwen3-32B)
and [vLLM structured-output documentation](https://docs.vllm.ai/en/latest/features/structured_outputs/).

## Frozen evaluation and review

```bash
uv run phil benchmark --suite benchmarks/heldout-v2.json --out outputs/evaluation
uv run phil audit outputs/evaluation --decisions PATH_TO_REVIEW.json --out outputs/audit
uv run phil verify-run outputs/evaluation --out outputs/lean-checks
```

`--workers 4` permits concurrent requests when the server can batch them. Each worker
has an isolated solver process. The suite file is saved with the run and hashed;
only each case's source text reaches the model. Review decisions are separate from
the generated artifact. See [fidelity-review.md](fidelity-review.md) for the protocol
and [acceptance.md](acceptance.md) for the completion gate.

The normalization contracts are conservative, partly lexical guards, not a semantic
classifier. They can reject an unusual but legitimate wording, and they do not catch
every way of dropping an unsupported operator. A successful run still requires source
review. Ambiguities, glossary notes and translation explanations are model proposals,
not verified philosophical commentary.
