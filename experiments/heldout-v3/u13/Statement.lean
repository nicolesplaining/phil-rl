import Lean

-- Formalization SHA256: 2314858bd19e8cd97ce0db70cb0222f24e0946a65f8fabe504cfe8a6eb1ec63e
-- Reconstruction SHA256: dc1c37b80c5fed102c2e17b2e011454f190d1ed9b6d707b9b0c21903c9ea9662
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_C : Prop) (s_W : Prop) : Prop :=
  (s_C → s_W) → s_C → s_W
