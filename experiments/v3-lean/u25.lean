import Lean

-- Formalization SHA256: 0319b43cb78e3f2bf3579802b5d65b9b385ccbd41120ccfee7d164245ff35a76
-- Reconstruction SHA256: c38d642cc3d58930d38a9abd1f5d5048a1cad83d832a4cf0f0fc37b1514bf273
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Testimony : Domain → Prop) (s_Deceives : Domain → Prop) (s_Trustworthy : Domain → Prop) : Prop :=
  (∀ s_x : Domain, (((s_Testimony s_x) ∧ (s_Deceives s_x)) → (¬ (s_Trustworthy s_x)))) → (∃ s_x : Domain, ((s_Testimony s_x) ∧ (s_Deceives s_x))) → (∃ s_x : Domain, ((s_Testimony s_x) ∧ (¬ (s_Trustworthy s_x))))
