import Lean

-- Formalization SHA256: 9e2a47c83f436ce0b8adb7e5de6693dfdfe1dc4201eecc3fddf9a58b35954d51
-- Reconstruction SHA256: 03db86e45ad413583ef6532ce572f934e5429aca686924be132c910ed0ac24be
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_C : Prop) (s_F : Prop) (s_D : Prop) : Prop :=
  (s_F → (¬ s_C)) → s_F → (¬ s_C)
