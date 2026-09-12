import Lean

-- Formalization SHA256: 896b71905fb4bfa2d41912ec1177980f1a0bd794e4ad635aed8cae464fd0af6e
-- Reconstruction SHA256: 36acafd27124988af2c394eb1b871b068e60454e2c9dbbfac5ef84c52c7621c6
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_M : Prop) (s_F : Prop) : Prop :=
  s_M → (¬ s_M) → s_F
