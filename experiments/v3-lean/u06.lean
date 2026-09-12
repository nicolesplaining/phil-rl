import Lean

-- Formalization SHA256: 9eb53c94df78560930efafcb527fc1132a2d6d1fda53a5e2270a0e971d792f25
-- Reconstruction SHA256: 67997ab017590c5b91e23f0618b9eb2c5e2791c6921e9a14e8fc2a3e9b9878a3
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_B : Prop) (s_P : Prop) : Prop :=
  (s_B ∨ s_P) → s_B → (¬ s_P)
