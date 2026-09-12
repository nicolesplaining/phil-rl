import Lean

-- Formalization SHA256: f847dc559aa4d74477c52ab56935eb2bbdfc96ab7462b624655766578945a9de
-- Reconstruction SHA256: be49b63997cf3dbd71be190a2f2b99d0b3cb6efa5a0934b1fa2a2cc1089447f0
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_DEF : Prop) (s_CON : Prop) : Prop :=
  (s_DEF → s_CON) → s_CON → s_DEF
