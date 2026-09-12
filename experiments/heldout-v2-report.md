# Second frozen evaluation

The second run also failed the acceptance gate. All 40 cases generated an outcome,
and all 32 supported cases matched their expected solver statuses. The strict
source/glossary audit nevertheless passed only 28 of 32 supported cases and 7 of 8
other cases. This illustrates why solver-status accuracy is not source fidelity.

Three supported non-passes, q12, q14 and q16, are legitimate ground-predicate
alternatives to propositional notation. They remain conservative non-passes under
the original protocol, not mistranslation labels. q22 has a real reconstruction
problem: it omits background and represents an opponent's statement as a reporting
fact rather than the opponent's asserted content.

The unsupported counterfactual q34 was flattened into material implication. The
longer objection regression also accepted modal claims under the fragment's
then-inadequate safeguards. Both raw runs remain preserved. The latter is an example
of why a schematic argument skeleton should not be presented as a complete modal
formalization, even when its conditional checker result is valid.

The next revision adds reversible Boolean abstraction for ground predicates without
quantifiers or equality. It stores the original formalization and checks that inverse
substitution exactly restores every formula. This is normalization, not a model
repair or a change to the source premises. Tests also check equivalence in Z3 under
the abbreviation definitions.

Modal guards, attribution handling and full source-unit coverage address the other
failures. All statements, including background, need a translation in a supported
artifact; a role label alone does not justify dropping a formula. These remain
conservative contracts rather than a complete semantic classifier.

V1 and V2 are now development sets. A third lexically new 40-case suite was specified
before inference. Many structures recur across sets, so none of these runs measures
generalization to an independent corpus of published philosophy.
