import Lean

-- Formalization SHA256: 882515576b9ba781d165dc9850df83db7f40ddcdc82b129f026cd42ceea4a640
-- Reconstruction SHA256: 631e5d0d00c61891d7baefe67ee89289a45e72cc3b1aa9f308a05c1cfe6518bb
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_P : Prop) (s_Q : Prop) (s_R : Prop) : Prop :=
  (s_P → s_Q) → s_P → (s_Q → s_R) → s_R
