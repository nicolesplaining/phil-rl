import Lean

-- Formalization SHA256: e74a6a0a060d7ff17c4621d3ec612ad48aca95b6361a5f274d91ef00ff68c779
-- Reconstruction SHA256: 41bac65c0fa6ae9f6d7512aed729773e6777d437e5e08846596b57273dd4ef6f
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Policy : Domain) (s_Equitable : Domain → Prop) (s_Popular : Domain → Prop) : Prop :=
  (s_Equitable s_Policy) → (¬ (s_Equitable s_Policy)) → (s_Popular s_Policy)
