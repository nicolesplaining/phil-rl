import Lean

-- Formalization SHA256: f3af5a26fd82bbb320120bf2a11f376d2948a46de8e0f1e3d71f7c93569a9880
-- Reconstruction SHA256: 631e5d0d00c61891d7baefe67ee89289a45e72cc3b1aa9f308a05c1cfe6518bb
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_E : Prop) (s_U : Prop) (s_N : Prop) : Prop :=
  (s_E → s_U) → s_E → (s_U → s_N) → s_N
