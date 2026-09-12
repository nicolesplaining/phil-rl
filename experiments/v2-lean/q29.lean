import Lean

-- Formalization SHA256: bb03731681a2500213699a5c304517bd810009579d69c100ca4108ececdbb885
-- Reconstruction SHA256: 03ee95e86bc5926a30b5eb25cd89ceadc021ddfd642cb559e2ce8e29900becf3
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Speaker : Domain) (s_Visitor : Domain) : Prop :=
  (s_Speaker = s_Visitor) → (s_Visitor = s_Speaker)
