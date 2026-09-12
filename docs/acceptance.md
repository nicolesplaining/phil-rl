# Working-version acceptance criteria

The active goal is a reliable first stage for short English philosophical arguments.
It must reconstruct the argument, preserve its meaning in the supported formal
language, and clearly identify cases that require interpretation or another logic.
It must not turn a valid proof of an altered argument into a fidelity claim.

## Scope

Inputs are short argumentative passages up to 20,000 characters, including objections,
missing premises, definitions, negation, conditionals, and quantifier scope. The
formal fragment is classical propositional logic and function-free, single-sorted
first-order logic. Modal, counterfactual, epistemic, and other unsupported inference
rules require an explicit decision to abstain or request review. Published papers,
PDF extraction, RL training, and philosophical-quality scoring are later stages.

## Required evidence for completion

1. All previous failures have regression coverage. Evidence references come from
   exact source spans; invalid quotes cannot produce accepted artifacts. Repairs
   preserve the frozen reconstruction and never receive proof success as a reward.
2. Completed runs and failures retain enough information to diagnose and reproduce
   every stage. Network errors, truncated generation, malformed JSON, no-argument
   inputs, oversized passages, and solver timeouts produce explicit outcomes.
3. The evaluation checks individual claims, premise roles, conditional direction,
   negation, scope, and declared symbol meanings. Matching a conclusion's solver
   status is insufficient. Unknown alignments count as unresolved, not correct.
4. A frozen suite of at least 40 new passages covers supported valid and invalid
   arguments, inconsistency, circularity, objections, implicit premises, ambiguity,
   and unsupported semantics. References must be written before model evaluation.
   At least 95% of supported cases must preserve the annotated formal meaning and
   active premises. Unsupported cases must not silently lose their operators.
5. The frozen evaluation stays distinct from development. If its failures guide
   changes, it becomes a regression set and a fresh evaluation is required. Report
   all runs, failures, abstentions and review decisions with denominators. These
   engineering annotations are not independent expert philosophical judgments.
6. Kernel-check every supported small propositional proof generated during final
   evaluation. Verify first-order statement exports and retain Z3 countermodels or
   unknown outcomes where applicable. A Lean definition never counts as a proof.
7. Run the finished CLI from a clean environment, verify CI, and replay the archived
   results. Preserve historical artifacts across schema changes. Record model,
   revision, inference configuration and the exact source/prompt versions.

The thresholds assess this bounded working version. They do not establish reliable
interpretation of arbitrary philosophy or remove the need for human review of novel
concepts. Do not mark the goal complete while a required check remains unmet.

## Operating constraints

Push directly to `main` with short lowercase conventional commits. Nicole Ma is the
sole author. Keep the README unchanged. Put documentation here and measured runs in
`experiments/`. Use only physical GPU 1 on the shared node, with isolated project
files, environment and port. Leave GPU 0 and its existing process alone.
