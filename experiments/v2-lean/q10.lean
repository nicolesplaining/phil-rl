import Lean

-- Formalization SHA256: 4d94e2f04339173b0dcc75da4e2809d405e711393f5b84e987739f477c06a6a3
-- Reconstruction SHA256: 6c7d4e3c3ed83c49ff1e67cfc58e6c9b47f2ab5a9ab26d3f3fc170a6c07c107b
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.

theorem argumentProof (s_D : Prop) (s_J : Prop) :
    (¬ (s_D → s_J)) → (s_D ∧ (¬ s_J)) := by
  classical
  by_cases h_D : s_D <;> by_cases h_J : s_J <;> simp_all

#print axioms argumentProof
