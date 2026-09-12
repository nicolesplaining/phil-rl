import Lean

-- Formalization SHA256: c49abc87abbec2961b8162e60c599a4a75d453436b330afe734b262bdceb2429
-- Reconstruction SHA256: cb120b9d8351ebd9d026f43766bdbf5d6dcbcdd7d4103a194d114efe2094c440
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_P : Prop) (s_Q : Prop) : Prop :=
  s_P → (¬ s_P) → s_Q
