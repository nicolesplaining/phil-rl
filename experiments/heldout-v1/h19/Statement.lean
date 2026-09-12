import Lean

-- Formalization SHA256: 1ad2bdc59d62ba9972814e1e7fb97bf3ad5fbf665825b18304e15db90a6cc69e
-- Reconstruction SHA256: dc2a4c4b044cbd45c55f1b695bc1c5cac50670491487730633e205d45533cf5e
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_FairContract : Prop) (s_CoercedContract : Prop) : Prop :=
  (s_CoercedContract → (¬ s_FairContract)) → s_CoercedContract → (¬ s_FairContract)
