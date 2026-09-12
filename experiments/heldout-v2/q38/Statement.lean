import Lean

-- Formalization SHA256: 64ad706cb874f225b3f311246e2c10f301e2cc61b30f90860b52ca339bd088b6
-- Reconstruction SHA256: bbe78358e4f1bb40b0afc98018300e211a35067294a9f0e66985773bce8c9c39
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Critic : Domain → Prop) (s_Theory : Domain → Prop) (s_Considered : Domain → Domain → Prop) : Prop :=
  (∀ s_x : Domain, ((s_Critic s_x) → (∃ s_y : Domain, ((s_Theory s_y) ∧ (s_Considered s_x s_y))))) → (∃ s_y : Domain, ((s_Theory s_y) ∧ (∀ s_x : Domain, ((s_Critic s_x) → (s_Considered s_x s_y)))))
