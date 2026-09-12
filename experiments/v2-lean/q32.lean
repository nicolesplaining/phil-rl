import Lean

-- Formalization SHA256: 946b5512c7959534225f6237f0d276af63135304c409e000a015585cfd7ef06f
-- Reconstruction SHA256: 6ea0374cc0dacd89c442f6263200d5fc03575e2800665fb5a3e063988a92e5bc
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Person : Domain → Prop) (s_Fallible : Domain → Prop) : Prop :=
  (∀ s_x : Domain, ((s_Person s_x) → (s_Fallible s_x))) → (∀ s_x : Domain, (((s_Person s_x) ∧ (¬ (s_Fallible s_x))) → (s_Fallible s_x)))
