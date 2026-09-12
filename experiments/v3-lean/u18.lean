import Lean

-- Formalization SHA256: 6b484ddba145e46283d729d68454b28d2b2a123a0156c9c16e36c31d5f180eda
-- Reconstruction SHA256: b52b273032a55c869dfb2557f0cd94d0242fcc12087e117dce466300462d50be
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.

theorem argumentProof (s_F : Prop) (s_R : Prop) :
    ((s_F ∨ s_R) ∧ (¬ (s_F ∧ s_R))) → s_F → (¬ s_R) := by
  classical
  by_cases h_F : s_F <;> by_cases h_R : s_R <;> simp_all

#print axioms argumentProof
