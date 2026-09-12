import Lean

-- Formalization SHA256: 4ae351a814800f1bde8d7f2f87f54549ac8707ff6dbb173a7ccd673343cf512f
-- Reconstruction SHA256: c1eb847ab654e159f30769ce3baba23e5dce22cff6e3705004790222b0cd10f2
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Justified : Domain → Prop) : Prop :=
  (¬ (∀ s_x : Domain, (s_Justified s_x))) → (∃ s_x : Domain, (¬ (s_Justified s_x)))
