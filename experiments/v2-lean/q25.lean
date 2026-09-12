import Lean

-- Formalization SHA256: 56d836698be5ff071ed82e9b3222e11d5a5454bce5d9fe93893363e429f5a548
-- Reconstruction SHA256: d0073a90b603486fcfdd531c13b798b789661b0558a011a277e1aab4d4255af2
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Statement : Domain → Prop) (s_Deceptive : Domain → Prop) (s_Sincere : Domain → Prop) : Prop :=
  (∀ s_x : Domain, (((s_Statement s_x) ∧ (s_Deceptive s_x)) → (¬ (s_Sincere s_x)))) → (∃ s_x : Domain, ((s_Statement s_x) ∧ (s_Deceptive s_x))) → (∃ s_x : Domain, ((s_Statement s_x) ∧ (¬ (s_Sincere s_x))))
