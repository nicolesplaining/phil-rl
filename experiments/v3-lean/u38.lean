import Lean

-- Formalization SHA256: 93d01d64b8c659e89a601ac3b5cbf8a33a7698fabc074762d988d5eeeb0cd31d
-- Reconstruction SHA256: da84c5c960a61031870a5af0e3de110ffa162a3b3adcb7a865ba2b6c4012e9a7
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Philosopher : Domain → Prop) (s_Examined : Domain → Domain → Prop) (s_Position : Domain → Prop) : Prop :=
  (∀ s_x : Domain, ((s_Philosopher s_x) → (∃ s_y : Domain, ((s_Position s_y) ∧ (s_Examined s_x s_y))))) → (∃ s_y : Domain, ((s_Position s_y) ∧ (∀ s_x : Domain, ((s_Philosopher s_x) → (s_Examined s_x s_y)))))
