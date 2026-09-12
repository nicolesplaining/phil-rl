import Lean

-- Formalization SHA256: e38c5ac3ff1ff33a9118b684678a60b960fb98499d1661ab2f6c96d4778888db
-- Reconstruction SHA256: 566830078f2cd3549cf51dad19944e68a5b1ae97a2bf1c890b001d28cab6184e
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Human : Domain → Prop) (s_Mortal : Domain → Prop) (s_Socrates : Domain) : Prop :=
  (∀ s_x : Domain, ((s_Human s_x) → (s_Mortal s_x))) → (s_Human s_Socrates) → (s_Mortal s_Socrates)
