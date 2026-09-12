import Lean

-- Formalization SHA256: a63f5af30dcc90793be5d877b4ae8a3d3f9d6f922379b564ef4ad745c0b61d75
-- Reconstruction SHA256: 309ccaa8f1705507df695c25834077df493382dd22d89fd7b9c889d80e9d90eb
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Person : Domain → Prop) (s_Trusts : Domain → Domain → Prop) : Prop :=
  (∀ s_x : Domain, ((s_Person s_x) → (∃ s_y : Domain, ((s_Person s_y) ∧ (s_Trusts s_x s_y))))) → (∃ s_y : Domain, ((s_Person s_y) ∧ (∀ s_x : Domain, ((s_Person s_x) → (s_Trusts s_x s_y)))))
