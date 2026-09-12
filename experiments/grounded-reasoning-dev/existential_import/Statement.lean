import Lean

-- Formalization SHA256: bfc286845188f11bf3ca7572faa7fa676b7ad2afe33f847e0d988b17b6de21ea
-- Reconstruction SHA256: 6c6fab22670e25d88a50873059de4ebef7ecfad7ca987b4bcf6702f9ff45d58a
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Human : Domain → Prop) (s_Mortal : Domain → Prop) : Prop :=
  (∀ s_x : Domain, ((s_Human s_x) → (s_Mortal s_x))) → (∃ s_x : Domain, (s_Human s_x))
