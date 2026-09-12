import Lean

-- Formalization SHA256: 449a063f401e8c277965aa16d5dbd6dfd025b04cf3c775037a940cdec3a01d21
-- Reconstruction SHA256: fe963607912838baf3bb77f349a2d82aece454261d11f861f7ee156bb8fabe8b
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_F : Prop) (s_T : Prop) : Prop :=
  (s_F → (¬ s_T)) → s_F → (¬ s_T)
