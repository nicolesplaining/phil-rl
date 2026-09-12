import Lean

-- Formalization SHA256: 168284534948d33906ec6cdfb9d4ad5b7b97977e828276d5f8df9d46adb4210a
-- Reconstruction SHA256: 34056418a0a812891ef84a7325efe804e2bb1382d13d7e378004741c4ade9d94
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_MRRequiresAP : Prop) (s_MoralResponsibility : Domain → Prop) (s_AlternativePossibilities : Domain → Prop) (s_AgentA : Domain) : Prop :=
  (s_MRRequiresAP → (∀ s_x : Domain, ((¬ (s_AlternativePossibilities s_x)) → (¬ (s_MoralResponsibility s_x))))) → (¬ (s_AlternativePossibilities s_AgentA)) → (s_MoralResponsibility s_AgentA) → (∃ s_x : Domain, ((s_MoralResponsibility s_x) ∧ (¬ (s_AlternativePossibilities s_x))))
