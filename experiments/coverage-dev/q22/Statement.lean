import Lean

-- Formalization SHA256: b67baff16ec097c9146ea696e48987bcbaf71c638199a5c8ab9f3bb991683471
-- Reconstruction SHA256: d60f5c8fb36b387178c2aed026882b606854e6561b6bb916213ac5a5072ff6a1
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_D : Prop) (s_R : Prop) (s_F : Prop) : Prop :=
  (s_F → (¬ s_R)) → s_F → (¬ s_R)
