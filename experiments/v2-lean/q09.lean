import Lean

-- Formalization SHA256: 9f2772a7e96bf96f9ebf444f0e76f2824fcb2ca3a38acbc23b7316a5632fff7e
-- Reconstruction SHA256: 587fa878751954d75fc5279e4a23281ea2309cdc3d6a538e0e1762fe0154517a
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.

theorem argumentProof (s_Informed : Prop) (s_Impartial : Prop) :
    (¬ (s_Informed ∧ s_Impartial)) → s_Informed → (¬ s_Impartial) := by
  classical
  by_cases h_Informed : s_Informed <;> by_cases h_Impartial : s_Impartial <;> simp_all

#print axioms argumentProof
