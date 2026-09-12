import Lean

-- Formalization SHA256: 3771d184ea0cb3618c2c013c496a2c9919443ae26f865877b26709c62f1d67a5
-- Reconstruction SHA256: 8876778469b5bc95e25de02e59434ed62cfa87708451f9f6d8f83d84c8053e75
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_L : Prop) (s_V : Prop) : Prop :=
  (s_L → s_V) → (¬ s_V) → (¬ s_L)
