import Lean

-- Formalization SHA256: a765d290eadd3ac293c42a19db104957a9d11f02f11bbbbf989b546a827dbb18
-- Reconstruction SHA256: dc37bc4c342439d54adac2c2ee4dbf26e596189f6708abfc002db7a4e35a22a5
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Person : Domain → Prop) (s_Reasons : Domain → Prop) (s_Fallible : Domain → Prop) (s_r : Domain) : Prop :=
  (∀ s_x : Domain, (((s_Person s_x) ∧ (s_Reasons s_x)) → (s_Fallible s_x))) → ((s_Person s_r) ∧ (s_Reasons s_r)) → (s_Fallible s_r)
