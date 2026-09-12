import Lean

-- Formalization SHA256: e49d97ba50d363b64de2586c4a9ea3e3e29137f5a5393a48bfc9494571060604
-- Reconstruction SHA256: 441cbfd860ff895bc98b26fd0a728b01feeb7d2eb3f3bcfa60f825eb467839e1
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Commitment : Domain → Prop) (s_Reason : Domain → Prop) (s_Sensation : Domain → Prop) : Prop :=
  (∀ s_x : Domain, ((s_Commitment s_x) → (s_Reason s_x))) → (∀ s_x : Domain, ((s_Reason s_x) → (¬ (s_Sensation s_x)))) → (∀ s_x : Domain, ((s_Commitment s_x) → (¬ (s_Sensation s_x))))
