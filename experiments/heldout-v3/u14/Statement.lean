import Lean

-- Formalization SHA256: 4e7764f22baea2d04208ce276275714e87914ebcffdf0a35b5b6bd04ba1d9ce5
-- Reconstruction SHA256: bfd2020016659e1ce8762de9f2e7e58cb93de57166fae6bd91f833e0aad0ad2a
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_Equitable : Prop) (s_Efficient : Prop) : Prop :=
  s_Equitable → (¬ s_Equitable) → s_Efficient
