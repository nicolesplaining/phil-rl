import Lean

-- Formalization SHA256: a2aaaa434ad7984f409e30a2195a1e7f6613dc40dd0ae740a0e33709d02a3e77
-- Reconstruction SHA256: f888477d270938a1b165fe14ea8bd7f9abd2004da7f64ac2b1a685c5bbdec57c
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Human : Domain → Prop) (s_Mortal : Domain → Prop) : Prop :=
  (∀ s_x : Domain, ((s_Human s_x) → (s_Mortal s_x))) → (∃ s_x : Domain, (s_Human s_x))
