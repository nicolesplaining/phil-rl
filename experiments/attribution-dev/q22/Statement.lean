import Lean

-- Formalization SHA256: cd2b0866233b9c4039434b1eb36dfd58dce71b50cd2c428270686a662a2f2b34
-- Reconstruction SHA256: a6a88238d6eed1c3f4d41b3a9deca2fb947985e735d397470f01406cb776a9c5
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_Trustworthy : Prop) (s_Fabricated : Prop) : Prop :=
  (s_Fabricated → (¬ s_Trustworthy)) → s_Fabricated → (¬ s_Trustworthy)
