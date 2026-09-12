import Lean

-- Formalization SHA256: 38b2151e0a0a8387b8cca94fbc6a66255f35bc723ea2983f3972e06eccfe6946
-- Reconstruction SHA256: 29140c35685b0c41fce8373dd01457d2148d65e9eeb4bb85c51b205444207aa3
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.

theorem argumentProof (s_E : Prop) (s_P : Prop) :
    ((s_E ∨ s_P) ∧ (¬ (s_E ∧ s_P))) → s_P → (¬ s_E) := by
  classical
  by_cases h_E : s_E <;> by_cases h_P : s_P <;> simp_all

#print axioms argumentProof
