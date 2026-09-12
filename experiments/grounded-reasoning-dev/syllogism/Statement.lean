import Lean

-- Formalization SHA256: e389fec4b10d535c8973bb75c17deffc4df36fbadb6da000eb34691e11dc07bf
-- Reconstruction SHA256: ee8c68c21d3500cf8567535dbe06c76a46e0341c08deec0c2cd35603b8857955
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Human : Domain → Prop) (s_Mortal : Domain → Prop) (s_Socrates : Domain) : Prop :=
  (∀ s_x : Domain, ((s_Human s_x) → (s_Mortal s_x))) → (s_Human s_Socrates) → (s_Mortal s_Socrates)
