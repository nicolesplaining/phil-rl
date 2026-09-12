import Lean

-- Formalization SHA256: cb717bbb85b5fe565d6ebf1fa62cc7586bb84bbf520dbaf0e6954c20669acf14
-- Reconstruction SHA256: dc8dd3de7a2c226137496b0724acc38fe4c0e18ad3846d155e1bf7297c9bd237
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_P : Prop) (s_Q : Prop) (s_R : Prop) : Prop :=
  (s_P → s_Q) → (s_Q → s_R) → (s_P → s_R)
