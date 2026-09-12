import Lean

-- Formalization SHA256: 6b968bf39c5e37328cb6d7c06c65d5a8130ebe591001eba2029cfd923504bdc8
-- Reconstruction SHA256: fd17916d75882555d7aea1e9b669fd1146927a9f32a8f097f857e1c8100f733f
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Desire : Domain → Prop) (s_Coherent : Domain → Prop) : Prop :=
  (¬ (∀ s_x : Domain, ((s_Desire s_x) → (s_Coherent s_x)))) → (∃ s_x : Domain, ((s_Desire s_x) ∧ (¬ (s_Coherent s_x))))
