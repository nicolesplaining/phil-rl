import Lean

-- Formalization SHA256: 22624d5a26fbe6cb613b9e503d0b0079cff3b302f0623553c90e6e608d8650fd
-- Reconstruction SHA256: 566830078f2cd3549cf51dad19944e68a5b1ae97a2bf1c890b001d28cab6184e
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Human : Domain → Prop) (s_Mortal : Domain → Prop) (s_socrates : Domain) : Prop :=
  (∀ s_x : Domain, ((s_Human s_x) → (s_Mortal s_x))) → (s_Human s_socrates) → (s_Mortal s_socrates)
