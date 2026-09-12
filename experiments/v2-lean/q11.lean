import Lean

-- Formalization SHA256: 39275e79afd6a00d663ed27c68df94d7030cb9a6143bd541343da6343a274e1f
-- Reconstruction SHA256: eefc43dc1147825439c8b84acdc4b3984ecd986e2c617032657eb387ae9a01c7
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.

theorem argumentProof (s_P : Prop) (s_Q : Prop) :
    (s_P ↔ s_Q) → (¬ s_Q) → (¬ s_P) := by
  classical
  by_cases h_P : s_P <;> by_cases h_Q : s_Q <;> simp_all

#print axioms argumentProof
