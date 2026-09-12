import Lean

-- Formalization SHA256: 5dc34cb5b90a684945c790c29653d0bfc27ed1268b547890a0161c216e43974d
-- Reconstruction SHA256: ebf688ac71e5ac35edf0df6c2eb1bf318a673522d0c776445bc50edea68e81a8
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_P : Prop) (s_Q : Prop) : Prop :=
  (s_P → s_Q) → (¬ s_P) → (¬ s_Q)
