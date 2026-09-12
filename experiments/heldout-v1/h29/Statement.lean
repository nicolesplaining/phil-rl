import Lean

-- Formalization SHA256: 4a5ec1490626f35bbb8111f443e4495065e441d98d0131c20bcb24d2dec6eb95
-- Reconstruction SHA256: c7775991c5ca8fcb7be0ebeb1934c9f5b84b8ea223bfdb0215aff429bb8ea6c7
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_T : Domain → Domain → Prop) : Prop :=
  (∀ s_x : Domain, (∃ s_y : Domain, (s_T s_x s_y))) → (∃ s_y : Domain, (∀ s_x : Domain, (s_T s_x s_y)))
