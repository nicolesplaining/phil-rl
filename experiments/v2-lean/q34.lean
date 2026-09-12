import Lean

-- Formalization SHA256: 70c54d96eeaae358aadc3528105484d8e7857e1dd3b1d87ac60939a82fe621ec
-- Reconstruction SHA256: 095f17e0ba0720e8dad5a106d575bf6d6ce7ed0dbbed7b5039f063688b4b6728
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.

theorem argumentProof (s_S : Prop) (s_D : Prop) :
    (s_S → s_D) → (¬ s_D) → (¬ s_S) := by
  classical
  by_cases h_S : s_S <;> by_cases h_D : s_D <;> simp_all

#print axioms argumentProof
