import Lean

-- Formalization SHA256: 1b40e668c61e82cf1d929dac9b49eec59d291d991ce69b242f005d5688b3a492
-- Reconstruction SHA256: 6347fa3d0e29e2c75c6328da164d12e84de9c45d546fc7844dc26315af8ff4c7
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.

theorem argumentProof (s_M : Prop) (s_F : Prop) :
    (s_M → s_F) → s_M → s_F := by
  classical
  by_cases h_M : s_M <;> by_cases h_F : s_F <;> simp_all

#print axioms argumentProof
