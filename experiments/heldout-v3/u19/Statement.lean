import Lean

-- Formalization SHA256: 054be2dde12fb93761ccb8aa21216cadc9eedfc4a6ed455d7cfc9c53396ea156
-- Reconstruction SHA256: d563f177ee6f095c405a511cd78ac03227b4fc1c0b0ed8531e3f3c440cad31a9
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_A : Prop) (s_B : Prop) : Prop :=
  s_A → (s_A ∨ s_B)
