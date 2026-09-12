# Reviewing source fidelity

A solver-status match is not a translation-quality score. The fidelity checker
requires a separate record of the reviewer's decisions about the source and glossary.
The current engineering review is agent-authored, not independent human validation.

The reviewer maps generated symbols to reference symbols after reading both English
meanings. The mapping must preserve kind and arity and be injective. It cannot add
logical connectives or define away a mistranslation. An unmappable symbol is a failed
or unresolved alignment, never an automatic success.

Claim groups permit splitting or merging conjunctions with the same role and source
coverage. Every explicit claim must appear exactly once. Each group's conjunction
must be equivalent in Z3, and the full set of active premises must also be equivalent.
This catches a dropped premise even when the conclusion happens to retain its status.
Unknown solver answers do not pass.

A model may explicitly choose a narrower individual domain. A reviewed unary domain
restriction can translate its quantifiers into the reference domain. The checker
also adds the narrow domain's nonemptiness and its constants' membership as generated
assumptions. Those assumptions must follow from the reference premises; otherwise
the comparison fails. Domain descriptions cannot excuse hidden existential import.

Unsupported and non-argument cases need direct source review, not formula comparison.
An ambiguous passage passes that category only if the system records the actual
alternative readings or abstains with a specific explanation. Circularity, premise
truth and validity alone are not linguistic ambiguities.

Keep reviews separate from immutable generated artifacts. Do not repair a generated
formula in the evaluation record. If a failed case guides a prompt or model change,
the whole suite becomes development data and a new held-out suite is required.
