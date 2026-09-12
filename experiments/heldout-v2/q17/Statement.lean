import Lean

-- Formalization SHA256: caf94642fc62c5668df8b4e55da27fa94cd9d61d56bad5a4ed1d6fd082c0c7e7
-- Reconstruction SHA256: d741a2cc5c6062bb0b9585f65dff2c15356c3361056bfd558c3ff141f589a6b5
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_F : Prop) (s_K : Prop) : Prop :=
  (s_F → (¬ s_K)) → s_F → (¬ s_K)
