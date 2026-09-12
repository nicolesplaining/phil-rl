import Lean

-- Formalization SHA256: 35338bde5002b456c226b4a1b26abe6d679c9ebc8bf38efd7a5df5e99126305a
-- Reconstruction SHA256: b72275264f43fffdc2e6044b62e69b03303f84a87083c8e91b0d947ce631ff30
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_V : Prop) : Prop :=
  (¬ (¬ s_V)) → s_V
