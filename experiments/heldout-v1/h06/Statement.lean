import Lean

-- Formalization SHA256: 3136132f7c37c8551c861cb726ff6262ac559dfdad6f4332d260a566d410a19c
-- Reconstruction SHA256: b2043e26e10174e47276045c112fc36fcdbbdcca656435dd0b7ec15307b57191
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_S : Prop) (s_A : Prop) : Prop :=
  (s_S ∨ s_A) → s_S → (¬ s_A)
