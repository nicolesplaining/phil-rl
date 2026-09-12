import Lean

-- Formalization SHA256: b61f32da8cf86ddea1d42a26b943a5f23c94abb26956f4377f74c1957bd9d9db
-- Reconstruction SHA256: 14ba6b4deaa6e3ca6bc8a3e62280cf069a5e6ee31a880d15556c1c28a93aca28
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_O : Prop) (s_F : Prop) : Prop :=
  ((s_O ∨ s_F) ∧ (¬ (s_O ∧ s_F))) → s_O → (¬ s_F)
