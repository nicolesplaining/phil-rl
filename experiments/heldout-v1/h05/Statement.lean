import Lean

-- Formalization SHA256: 594d352220560e39295becff5726f64db74d066c184aea71ce0a098c89176326
-- Reconstruction SHA256: bd05812970e6e8f77bed7b4ea698ef7a506cbf676306f14ab89759df7bb96ca5
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_P : Prop) (s_Q : Prop) : Prop :=
  (s_P ∨ s_Q) → (¬ s_P) → s_Q
