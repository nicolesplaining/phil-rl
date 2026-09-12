import Lean

-- Formalization SHA256: 7e5fa1e08e95af45f13263b0a0f828b7aefbb4099cbad9db05f10bb393c0d025
-- Reconstruction SHA256: 033470dfd1560908351b75ecb51f2f8d90ff974f5f0e99db9e6ba40abe33ad76
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Person : Domain → Prop) (s_Deliberates : Domain → Prop) (s_Reflective : Domain → Prop) (s_Neri : Domain) : Prop :=
  (∀ s_x : Domain, (((s_Person s_x) ∧ (s_Deliberates s_x)) → (s_Reflective s_x))) → ((s_Person s_Neri) ∧ (s_Deliberates s_Neri)) → (s_Reflective s_Neri)
