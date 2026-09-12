import Lean

-- Formalization SHA256: b7e729e639498840898a4a0a05def2ba182d302880655a42e8c3ee42ddf27b06
-- Reconstruction SHA256: fcbda8b30d1bac7529f5cb54ce9b9f3d9b3213f52501e2a0352b961ebd2b8f16
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Reader : Domain → Prop) (s_Book : Domain → Prop) (s_Admired : Domain → Domain → Prop) : Prop :=
  (∀ s_x : Domain, ((s_Reader s_x) → (∃ s_y : Domain, ((s_Book s_y) ∧ (s_Admired s_x s_y))))) → (∃ s_y : Domain, ((s_Book s_y) ∧ (∀ s_x : Domain, ((s_Reader s_x) → (s_Admired s_x s_y)))))
