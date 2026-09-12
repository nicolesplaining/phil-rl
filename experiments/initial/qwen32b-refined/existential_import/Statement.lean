import Lean

-- Formalization SHA256: 8737a837931b6457a6958f05a3be8e071f9c7089a374ebc536fbbfa4f55ccb43
-- Reconstruction SHA256: 3af12cf209713c73af377e6c8297018a81fa6dd2a67c31bb0a2460309aba3e28
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Human : Domain → Prop) (s_Mortal : Domain → Prop) : Prop :=
  (∀ s_x : Domain, ((s_Human s_x) → (s_Mortal s_x))) → (∃ s_x : Domain, (s_Human s_x))
