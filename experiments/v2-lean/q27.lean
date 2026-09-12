import Lean

-- Formalization SHA256: 2997bd3ceb0588175ea6a76628fa4c2ca0fba0d81f98cb6a1450ecbce61cbb85
-- Reconstruction SHA256: 5b3b47107352c7af07c7d1fdff38c0943d800270563dd3ecd06f638ce96bc037
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Agent : Domain → Prop) (s_Defers : Domain → Domain → Prop) : Prop :=
  (∀ s_x : Domain, ((s_Agent s_x) → (∃ s_y : Domain, ((s_Agent s_y) ∧ (s_Defers s_x s_y))))) → (∃ s_y : Domain, ((s_Agent s_y) ∧ (∀ s_x : Domain, ((s_Agent s_x) → (s_Defers s_x s_y)))))
