import Lean

-- Formalization SHA256: 17997c27a10c85a8758a570881f93f6bb7e71699abf8e51f2993b2d76a720011
-- Reconstruction SHA256: edb3f830a139241880d4bea2314fba7f6eaff8f64a1b1bef0e10b8c89e93fb2a
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Person : Domain → Prop) (s_SelfIdentical : Domain → Prop) : Prop :=
  (∀ s_x : Domain, ((s_Person s_x) → (s_SelfIdentical s_x))) → (∀ s_x : Domain, ((s_Person s_x) → (s_SelfIdentical s_x)))
