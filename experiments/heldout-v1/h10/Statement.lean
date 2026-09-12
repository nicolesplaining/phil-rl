import Lean

-- Formalization SHA256: 706caeabdb1c9bc96f31c537a6868bac43cc9025e6e5417ab5c28f091826dd9b
-- Reconstruction SHA256: e9f75d8c1c1085d36428249ef51791ac156f775128521b3a05f32b958cd61adf
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_C1 : Prop) (s_C2 : Prop) (s_C3 : Prop) : Prop :=
  s_C1 → s_C2 → s_C2
