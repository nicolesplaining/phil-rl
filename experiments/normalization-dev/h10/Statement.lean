import Lean

-- Formalization SHA256: c5f1440d4690ef10005223e6c857f62aa6b081471a3a417294548d1bea2b0ae9
-- Reconstruction SHA256: cd0ed297db7c586d3d6c5958f14d11ad4714e53ec5eefd8ea676cfc8fc0a002b
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_Complete : Prop) (s_Circular : Prop) : Prop :=
  ((¬ s_Complete) ∧ (¬ s_Circular)) → (¬ s_Circular)
