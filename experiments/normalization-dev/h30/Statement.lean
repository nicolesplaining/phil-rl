import Lean

-- Formalization SHA256: 1fb5065c90e4fef050725a292a9d8f840de9ed834ef12bcd512e70e8704b3675
-- Reconstruction SHA256: 97e49ab0a8be6a2d3b24e54fb789ba88e1508b143d2cf0e8745e3f62c304a281
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_lina : Domain) (s_witness : Domain) (s_Honest : Domain → Prop) : Prop :=
  (s_lina = s_witness) → (s_Honest s_witness) → (s_Honest s_lina)
