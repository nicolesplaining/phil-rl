import Lean

-- Formalization SHA256: 47d3f692450b681fe94739189ee0ecabf6ab46f3cf792f87f9f62e322485b2b6
-- Reconstruction SHA256: f4676a662bb14c133fadbeff6a1fc4292ac7853cb1058d312e5fb4b4b2eca0af
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.

theorem argumentProof (s_C : Prop) (s_A : Prop) :
    (s_C ↔ s_A) → (¬ s_A) → (¬ s_C) := by
  classical
  by_cases h_C : s_C <;> by_cases h_A : s_A <;> simp_all

#print axioms argumentProof
