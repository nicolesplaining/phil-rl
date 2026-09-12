import Lean

-- Formalization SHA256: 449f9d1fb2071bac0434836b34627146555bc2987a5117e6ad3d5717c15969db
-- Reconstruction SHA256: 4e1dab2c0242f15c16bc15e04737435eb5f70607b9a86aaa7d0127a4e5c3d95c
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Admires : Domain → Domain → Prop) : Prop :=
  (∀ s_x : Domain, (∃ s_y : Domain, (s_Admires s_x s_y))) → (∃ s_y : Domain, (∀ s_x : Domain, (s_Admires s_x s_y)))
