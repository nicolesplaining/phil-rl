import Lean

-- Formalization SHA256: 2718de090973d9177880f1f826dab2e51ce533d46fad6f4b6a4cd7ef5096d0fe
-- Reconstruction SHA256: 63756ab479a696f439184a9255104c350b44c2c5134cc7b410184661522874d9
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_R : Domain → Domain → Prop) : Prop :=
  (∃ s_x : Domain, (∀ s_y : Domain, (s_R s_x s_y))) → (∀ s_y : Domain, (∃ s_x : Domain, (s_R s_x s_y)))
