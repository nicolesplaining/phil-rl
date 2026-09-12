import Lean

-- Formalization SHA256: 6b484ddba145e46283d729d68454b28d2b2a123a0156c9c16e36c31d5f180eda
-- Reconstruction SHA256: b52b273032a55c869dfb2557f0cd94d0242fcc12087e117dce466300462d50be
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_F : Prop) (s_R : Prop) : Prop :=
  ((s_F ∨ s_R) ∧ (¬ (s_F ∧ s_R))) → s_F → (¬ s_R)
