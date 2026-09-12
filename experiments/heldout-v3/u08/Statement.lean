import Lean

-- Formalization SHA256: 57c89895eace9cb7e7353de6fc2c0cdfdf55b692940660c8503bfdff3cbd13cf
-- Reconstruction SHA256: f190359a225857821f29192139754616adc52f901ce339c755804517ac5aaef6
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_P : Prop) (s_Q : Prop) : Prop :=
  (¬ s_P) → (¬ s_Q) → (¬ s_Q)
