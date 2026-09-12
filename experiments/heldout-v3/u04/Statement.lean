import Lean

-- Formalization SHA256: 74d722630a81f60eaf410bb72bfafe0242514c4faab2c9823244fd7417ab5ffe
-- Reconstruction SHA256: 44c7f5732918a47e4c2418cfedf96d6a493ff101567144398429a0fd9ed3e32e
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_R : Prop) (s_Q : Prop) : Prop :=
  (s_R → s_Q) → (¬ s_R) → (¬ s_Q)
