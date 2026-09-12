import Lean

-- Formalization SHA256: 288d33378bdc6f555f21b003b0d1e6a24bc0262cc1e63a4046e629243843933d
-- Reconstruction SHA256: 6407f4b4cf20c6c07d76fc5c5f648ffb2070abb4647ee700b0be800b865c1c99
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_MR : Prop) (s_FA : Prop) : Prop :=
  (s_MR → s_FA) → s_FA → s_MR
