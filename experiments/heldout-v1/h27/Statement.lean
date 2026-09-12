import Lean

-- Formalization SHA256: 0ee69cee1140d0690617d13973c6b5b1dd33351d3f83bd4fa03a5f872808df7b
-- Reconstruction SHA256: d33aff3de05a73d3ea515a2815e763e9ae4de1bd18fc87e5b96d4746a379ce11
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Coercive : Domain → Prop) (s_Voluntary : Domain → Prop) : Prop :=
  (∀ s_x : Domain, ((s_Coercive s_x) → (¬ (s_Voluntary s_x)))) → (∃ s_x : Domain, (s_Coercive s_x)) → (∃ s_x : Domain, (¬ (s_Voluntary s_x)))
