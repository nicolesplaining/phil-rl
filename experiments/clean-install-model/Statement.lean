import Lean

-- Formalization SHA256: d8bb21f1efb4759994e8946a8fbf765e92612205d0821fbfb6f211ed64815ca0
-- Reconstruction SHA256: ae084a3a5e9f1ac4bb7d81a50ea1528331ae393640f961c15898f530ed3e89d4
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_R : Prop) (s_F : Prop) : Prop :=
  (s_R → s_F) → s_R → s_F
