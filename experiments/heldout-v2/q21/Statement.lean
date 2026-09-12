import Lean

-- Formalization SHA256: 0dabc5b85ae11c67fe654fb7b2034462431e922cb4329067a3adbb048319e8ee
-- Reconstruction SHA256: fa81bccbe945a6040055404ba8e11676de7d0c0563328f7bb7187614ff448e4b
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_CommitteeDiscussing : Prop) (s_Deception : Prop) (s_Informed : Prop) (s_Legitimate : Prop) : Prop :=
  (s_Deception → (¬ s_Informed)) → s_Deception → ((¬ s_Informed) → (¬ s_Legitimate)) → (¬ s_Legitimate)
