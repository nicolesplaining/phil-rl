import Lean

-- Formalization SHA256: 2a05cd1883c599be2f18af1a06ba9d2bcd18ea59d3f243950140761c31661d4a
-- Reconstruction SHA256: 486e478b2c76e12ba1762ba0a732c02a21a3864f7caeedac8b09ff994a7599eb
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Ivo : Domain) (s_author : Domain) (s_Candid : Domain → Prop) : Prop :=
  (s_Ivo = s_author) → (s_Candid s_author) → (s_Candid s_Ivo)
