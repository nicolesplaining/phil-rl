import Lean

-- Formalization SHA256: a5215afa80a0db89b081926f71c41e014aff5306f50e6f959d69a45517d7811c
-- Reconstruction SHA256: bbe57930a514473d670a821158776ea3c45411ec256cdae64beeadbd821d112e
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Admires : Domain → Domain → Prop) : Prop :=
  (∀ s_x : Domain, (∃ s_y : Domain, (s_Admires s_x s_y))) → (∃ s_y : Domain, (∀ s_x : Domain, (s_Admires s_x s_y)))
