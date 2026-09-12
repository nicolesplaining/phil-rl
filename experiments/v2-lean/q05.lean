import Lean

-- Formalization SHA256: 16ba127ce0ac74c94ac7e86f5133c9544eb2460c93b4a225d69d04b9d2b7b77c
-- Reconstruction SHA256: 2194aec50abf22911545ddea36b03b11061005d703c66741dd256477ef2a0c7c
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.

theorem argumentProof (s_P : Prop) (s_Q : Prop) :
    (s_P ∨ s_Q) → (¬ s_P) → s_Q := by
  classical
  by_cases h_P : s_P <;> by_cases h_Q : s_Q <;> simp_all

#print axioms argumentProof
