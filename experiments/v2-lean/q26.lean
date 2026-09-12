import Lean

-- Formalization SHA256: a88c877ad00617c108ec4be0dcaa6d8ff15877208122df736f24baf726d1117e
-- Reconstruction SHA256: 8a66910e451fd95d0a2e7f1b41067248898eceff977eeef6c5202fccc48cce23
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Interpretation : Domain → Prop) (s_Coherent : Domain → Prop) : Prop :=
  (¬ (∀ s_x : Domain, ((s_Interpretation s_x) → (s_Coherent s_x)))) → (∃ s_x : Domain, ((s_Interpretation s_x) ∧ (¬ (s_Coherent s_x))))
