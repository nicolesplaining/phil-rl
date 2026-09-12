import Lean

-- Formalization SHA256: a47413b513d6488ba4bcf53d9c3f1664488d7461861ccd9d3e872b9d1bf08229
-- Reconstruction SHA256: ca9643d8b0a6b00d2544c09ad29820ac7a90582c87fcb5362db269e48474e715
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_F : Prop) (s_E : Prop) : Prop :=
  (¬ (s_F ∧ s_E)) → s_F → (¬ s_E)
