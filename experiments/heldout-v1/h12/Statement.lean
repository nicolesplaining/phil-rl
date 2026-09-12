import Lean

-- Formalization SHA256: 3a0dd5abd037c96649c99ee7e8cf156a53914b5bf2c228f5ca581c7fafa664b2
-- Reconstruction SHA256: 6ca5ea6ff51dd8859c606794f2ee3b906c502a4eae88e5ca757da2bad49c0868
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_A : Prop) (s_C : Prop) : Prop :=
  ((¬ s_C) → s_A) → (¬ s_C) → s_A
