import Lean

-- Formalization SHA256: 776f58e392330509fe97a0de466ce427ab3655917902b075e7097a1ef3a256e5
-- Reconstruction SHA256: aae2b71451bb528d5ee4826985e2a690d2551219573421eae010c473d4cc111f
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Genuine : Domain → Prop) (s_Informed : Domain → Prop) (s_c : Domain) : Prop :=
  (∀ s_x : Domain, ((s_Genuine s_x) → (s_Informed s_x))) → (¬ (s_Informed s_c)) → (¬ (s_Genuine s_c))
