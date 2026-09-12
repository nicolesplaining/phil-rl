import Lean

-- Formalization SHA256: 6c14cecc136f9d4971706305565e2d9c9a286a59023309c1f0a9c4a1c5e35843
-- Reconstruction SHA256: 2dbbad2e1556640a67eb7a30de4a96deba3d359fdb420d16621d38703eff2278
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_D : Prop) (s_U : Prop) (s_S : Prop) : Prop :=
  (s_D → s_U) → s_D → s_U
