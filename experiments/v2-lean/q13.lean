import Lean

-- Formalization SHA256: 56a362ac14334f06338f8be983723307ccae5acac5b44bc5d1c66f0270c09535
-- Reconstruction SHA256: 7a5b91659ba3e51fb8e53323c094a9498d0ed64ed60a32d784ca46c960673723
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.

theorem argumentProof (s_G : Prop) (s_W : Prop) :
    (s_G → s_W) → s_G → s_W := by
  classical
  by_cases h_G : s_G <;> by_cases h_W : s_W <;> simp_all

#print axioms argumentProof
