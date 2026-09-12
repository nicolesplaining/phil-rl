import Lean

-- Formalization SHA256: 2f7848e90ad9d8f791809e9b03ecbe8d25ff07f8ac3caf7ede120b45c4828071
-- Reconstruction SHA256: 7a1b0a89cc5927fd70c6111b367d88234163eeea6334ce0a2b6b712e60014753
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.

theorem argumentProof (s_R : Prop) (s_M : Prop) :
    (s_R ∨ s_M) → (¬ s_R) → s_M := by
  classical
  by_cases h_R : s_R <;> by_cases h_M : s_M <;> simp_all

#print axioms argumentProof
