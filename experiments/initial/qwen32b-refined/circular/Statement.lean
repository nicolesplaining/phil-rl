import Lean

-- Formalization SHA256: 71fc10066ecf38b351fc9105cb5767f23c255722dfd43f3c1ab392adc6ada7ab
-- Reconstruction SHA256: 2d6b7fd54e5125cc106c0e4cff0284dba24abbdc5ca9cc0af1f6b344e54b46ee
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_FreeAction : Prop) : Prop :=
  s_FreeAction → s_FreeAction
