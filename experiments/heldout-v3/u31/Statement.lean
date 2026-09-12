import Lean

-- Formalization SHA256: 208b3125636ca5b3341013c3ca9559530ea2b2737f5052db8cf12680e38b3e7c
-- Reconstruction SHA256: 6b31715e0603dc712dc9dc6ac7bad2097a2917c8201b0c7f89d3707558074c04
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Interpreter : Domain → Prop) (s_Questions : Domain → Domain → Prop) : Prop :=
  (∃ s_x : Domain, ((s_Interpreter s_x) ∧ (∀ s_y : Domain, ((s_Interpreter s_y) → (s_Questions s_x s_y))))) → (∀ s_y : Domain, ((s_Interpreter s_y) → (∃ s_x : Domain, ((s_Interpreter s_x) ∧ (s_Questions s_x s_y)))))
