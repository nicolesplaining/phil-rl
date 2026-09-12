import Lean

-- Formalization SHA256: 6e188df654526eac1fb800c7de60dc0725fc061b66685aea406143d7111e5bb5
-- Reconstruction SHA256: 31f1ac6e922bfb954876bc9784f127461bff3c4a58435343d1d6463e2271cac0
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Consents : Domain → Prop) (s_Informed : Domain → Prop) (s_mira : Domain) : Prop :=
  (∀ s_x : Domain, ((s_Consents s_x) → (s_Informed s_x))) → (s_Consents s_mira) → (s_Informed s_mira)
