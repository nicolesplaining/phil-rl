import Lean

-- Formalization SHA256: 9d453a6906ca0090e2d2bf82b6d9058fec9ae69a51e12c611fae0b94d23edee2
-- Reconstruction SHA256: 7df08054bac6c4dbee3596e13cf66fd6f1589ddaac739680e7f3b23d844b2777
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_MR : Prop) (s_FA : Prop) : Prop :=
  (s_MR → s_FA) → s_MR → s_FA
