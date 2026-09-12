import Lean

-- Formalization SHA256: 50efa2e88f4a27e6fe27def2a54bfa7331f6a6bdf25f707a3f6cce06833a3432
-- Reconstruction SHA256: d66d9d3a713591830705e938df900ed52a51954cceb5f2fdbd5c8927613a4cdb
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.

theorem argumentProof (s_L : Prop) (s_I : Prop) :
    (s_L → s_I) → (¬ s_I) → (¬ s_L) := by
  classical
  by_cases h_L : s_L <;> by_cases h_I : s_I <;> simp_all

#print axioms argumentProof
