import Lean

-- Formalization SHA256: 7d1a95059d3e465dfb80bf2ff3898da87579a92b913b6c7533b9ad5c386e6986
-- Reconstruction SHA256: 6d20613c199c850f26dce7061d654c14a841638888ab9dcc30e1bf1bdf8cd865
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.

theorem argumentProof (s_P : Prop) (s_Q : Prop) :
    (¬ (s_P ∧ s_Q)) → s_P → (¬ s_Q) := by
  classical
  by_cases h_P : s_P <;> by_cases h_Q : s_Q <;> simp_all

#print axioms argumentProof
