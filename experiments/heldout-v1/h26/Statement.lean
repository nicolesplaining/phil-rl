import Lean

-- Formalization SHA256: 69699db37fda4f9a4544b8b97078def9606798fd94b05e9c5eeab775d9c0985b
-- Reconstruction SHA256: 3188a48b8d21540c5eb9be83ef0f13a7ed7dcb2baf4fa5db1c64a62c1c79e45d
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_PerfectJudge : Domain → Prop) (s_Impartial : Domain → Prop) : Prop :=
  (∀ s_x : Domain, ((s_PerfectJudge s_x) → (s_Impartial s_x))) → (∃ s_x : Domain, ((s_PerfectJudge s_x) ∧ (s_Impartial s_x)))
