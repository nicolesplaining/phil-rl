import Lean

-- Formalization SHA256: 33be70c511dbb56b3b8230adfd341a20e17f50f3dad4eae0aa12ec80a1a3145e
-- Reconstruction SHA256: 627ffc4c7148ebed3223ab109a814ab5d723f68d638b269d995f4a65ffb60ef2
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.

theorem argumentProof (s_V : Prop) (s_A : Prop) :
    (¬ (s_V ∨ s_A)) → (¬ s_A) := by
  classical
  by_cases h_V : s_V <;> by_cases h_A : s_A <;> simp_all

#print axioms argumentProof
