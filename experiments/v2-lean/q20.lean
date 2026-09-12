import Lean

-- Formalization SHA256: 6bcc4ac57ec7151d0b03ac111f1213747a7829a8db03dd6bdbd6f21351623038
-- Reconstruction SHA256: 0b51ca855628107f189a7e36bffb7cec0a7fdb5fd15a1a7795d85f6a94c84081
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.

theorem argumentProof (s_F : Prop) (s_J : Prop) :
    (s_F → s_J) → ((¬ s_F) → s_J) → s_J := by
  classical
  by_cases h_F : s_F <;> by_cases h_J : s_J <;> simp_all

#print axioms argumentProof
