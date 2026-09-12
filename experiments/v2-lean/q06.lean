import Lean

-- Formalization SHA256: 1919f3d4321a5599df16da8bfae94dd3a8a2fd40c2c6696a222b87ddbef11af0
-- Reconstruction SHA256: 5d1445f37c56a0341f6e4cd640de5f96ea5422834b4c5722269a40ba973749ea
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_A : Prop) (s_P : Prop) : Prop :=
  (s_A ∨ s_P) → s_A → (¬ s_P)
