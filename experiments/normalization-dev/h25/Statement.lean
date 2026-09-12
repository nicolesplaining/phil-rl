import Lean

-- Formalization SHA256: 79f7050654da40baf3c7f035ed74fb566dcc3ea2e39f417f783ed1ba4e2ce995
-- Reconstruction SHA256: 8f2fbdd294b49df953a45dacdec9199e81e6dd38ddfbd0f4c7e9d238404d1567
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Person : Domain → Prop) (s_Consents : Domain → Prop) (s_Informed : Domain → Prop) (s_Mira : Domain) : Prop :=
  (∀ s_x : Domain, (((s_Person s_x) ∧ (s_Consents s_x)) → (s_Informed s_x))) → ((s_Person s_Mira) ∧ (s_Consents s_Mira)) → (s_Informed s_Mira)
