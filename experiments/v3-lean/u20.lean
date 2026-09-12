import Lean

-- Formalization SHA256: fa2f5fb933f94a8f138d82bd360406f85c6909d8d9af75eb0d98605bf49a495c
-- Reconstruction SHA256: d69714b7e389ff03d0db0ab52479579434085f8ee3728deb51e4c98203f17636
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.

theorem argumentProof (s_A : Prop) (s_R : Prop) :
    (s_A → s_R) → ((¬ s_A) → s_R) → s_R := by
  classical
  by_cases h_A : s_A <;> by_cases h_R : s_R <;> simp_all

#print axioms argumentProof
