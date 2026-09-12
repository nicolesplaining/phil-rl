import Lean

-- Formalization SHA256: 16e97bcf835ee2580cf0c2d4042f303bf319cbf3acc5e24c0792a03fcc471c8a
-- Reconstruction SHA256: e6998cd394710a0727ee3b4488062bb4f09b888fba7c9f54e61a901c499cba1a
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_P : Prop) (s_Q : Prop) (s_R : Prop) : Prop :=
  (s_P → s_Q) → s_P → (s_Q → (¬ s_R)) → (¬ s_R)
