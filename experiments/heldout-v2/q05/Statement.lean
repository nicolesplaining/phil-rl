import Lean

-- Formalization SHA256: 16ba127ce0ac74c94ac7e86f5133c9544eb2460c93b4a225d69d04b9d2b7b77c
-- Reconstruction SHA256: 2194aec50abf22911545ddea36b03b11061005d703c66741dd256477ef2a0c7c
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_P : Prop) (s_Q : Prop) : Prop :=
  (s_P ∨ s_Q) → (¬ s_P) → s_Q
