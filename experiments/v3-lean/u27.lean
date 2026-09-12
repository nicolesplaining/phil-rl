import Lean

-- Formalization SHA256: fa176119367d6d00760e0a64ed86f7204bde290be1c7bba7500d49cacc16be8a
-- Reconstruction SHA256: 6b6da527f764890dc02fec981c713f3f7b8c66c49a83584ee589c51a23d52c63
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Scholar : Domain → Prop) (s_Consults : Domain → Domain → Prop) : Prop :=
  (∀ s_x : Domain, ((s_Scholar s_x) → (∃ s_y : Domain, ((s_Scholar s_y) ∧ (s_Consults s_x s_y))))) → (∃ s_y : Domain, ((s_Scholar s_y) ∧ (∀ s_x : Domain, ((s_Scholar s_x) → (s_Consults s_x s_y)))))
