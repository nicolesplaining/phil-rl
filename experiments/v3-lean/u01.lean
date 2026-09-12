import Lean

-- Formalization SHA256: 34359344d8850a694a56230daa5d4bda7d1cc2e5518e88dd0ea0912daad22bcd
-- Reconstruction SHA256: e55f4e2a6c53b8222bcce2d101c078d4e0a2fd4a7c4e2e7e66070687b632b72b
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.

theorem argumentProof (s_P : Prop) (s_Q : Prop) :
    (s_P → s_Q) → s_P → s_Q := by
  classical
  by_cases h_P : s_P <;> by_cases h_Q : s_Q <;> simp_all

#print axioms argumentProof
