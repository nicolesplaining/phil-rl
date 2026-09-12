import Lean

-- Formalization SHA256: 018c56cf31e1e323882b64966fe69ecd39ac62583b0170163c84e379ff7aaceb
-- Reconstruction SHA256: 2c7bd9db306a29e93f1ab1f62a3dedf5ead10f4435acadb155e548edf7da0adc
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_E : Prop) (s_B : Prop) : Prop :=
  (s_E → s_B) → (¬ s_E) → (¬ s_B)
