import Lean

-- Formalization SHA256: a9df2b21237c4d15789ad6572e060d549bf84fd8b542325afedf8a7d14492a9a
-- Reconstruction SHA256: e2b0af34aa810657b951fd9a2a6ef6ef8c0298ee4d2fd1595cf1ecbb3ab88e2a
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Honest : Domain → Prop) (s_Truthful : Domain → Prop) (s_Rowan : Domain) : Prop :=
  (∀ s_x : Domain, ((s_Honest s_x) → (s_Truthful s_x))) → (s_Honest s_Rowan) → (s_Truthful s_Rowan)
