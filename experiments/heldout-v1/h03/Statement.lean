import Lean

-- Formalization SHA256: 9a4ef53ae5a7113aae07888f4fe065222c1ebaf725c01edaf1cedf6a930ca4a6
-- Reconstruction SHA256: 1f686955292576523d1af5784adcfe29a4016ebc62317291f80d048c36012fc5
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_A : Prop) (s_D : Prop) : Prop :=
  (s_A → s_D) → s_D → s_A
