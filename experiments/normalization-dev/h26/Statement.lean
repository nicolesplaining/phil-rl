import Lean

-- Formalization SHA256: 2db69a0b07f9dce6ffa12dc7bebd7b807be43bd20603ee4cd802fefc3b59691c
-- Reconstruction SHA256: 3bf2b842c5a5825ab745c8ae53a56f41d38a4a9f4d3741683aa3c6fda8a5ee7f
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_PerfectJudge : Domain → Prop) (s_Impartial : Domain → Prop) : Prop :=
  (∀ s_x : Domain, ((s_PerfectJudge s_x) → (s_Impartial s_x))) → (∃ s_x : Domain, ((s_PerfectJudge s_x) ∧ (s_Impartial s_x)))
