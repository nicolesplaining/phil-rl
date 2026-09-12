import Lean

-- Formalization SHA256: 71b2e070cb9dbc1dc6baf8e450e2f8553e47dc4d945eefcbb5d75b4bdc023284
-- Reconstruction SHA256: 0a7226507278a27f5bd6b6cdcf4c08ef13b34c9479888132dfaccf98629de45f
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.

theorem argumentProof (s_R : Prop) (s_E : Prop) :
    (s_R → (¬ s_E)) → s_R → (¬ s_E) := by
  classical
  by_cases h_R : s_R <;> by_cases h_E : s_E <;> simp_all

#print axioms argumentProof
