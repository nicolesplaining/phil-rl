import Lean

-- Formalization SHA256: c51ebaf7b7045d9dd5566c774f2655a24b6c949f6925b7d32c562b3e047a21e6
-- Reconstruction SHA256: a8a833e5e008eabca46e04d5790a339be4c276d76dcef716c2e9a571e091c00b
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.

theorem argumentProof (s_c1 : Prop) (s_c2 : Prop) :
    s_c1 → s_c2 → (s_c1 ∧ s_c2) := by
  classical
  by_cases h_c1 : s_c1 <;> by_cases h_c2 : s_c2 <;> simp_all

#print axioms argumentProof
