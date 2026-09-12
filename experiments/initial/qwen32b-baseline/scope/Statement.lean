import Lean

-- Formalization SHA256: 16ca53f250ccee994d8617e0b4e83a9cff93c585a59bd01bc46304f4ccaa460f
-- Reconstruction SHA256: 4deb7d6f850ae74ff28a1562f9f6147d47ee8bd195f8bc6da7051c29bd18e16e
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Admires : Domain → Domain → Prop) : Prop :=
  (∀ s_x : Domain, (∃ s_y : Domain, (s_Admires s_x s_y))) → (∃ s_y : Domain, (∀ s_x : Domain, (s_Admires s_x s_y)))
