import Lean

-- Formalization SHA256: 1638f6401838c091bc607966f1386d011195acb2814a1a0fd6b5fd35a51e0195
-- Reconstruction SHA256: 1d8e6cfefcd5bb1e1bf542faf714b287c9a813f0a070a618d071fc3196905a80
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_V : Domain → Prop) (s_A : Domain → Prop) (s_Val : Domain → Prop) : Prop :=
  (∀ s_x : Domain, ((s_V s_x) → (s_A s_x))) → (∀ s_x : Domain, ((s_A s_x) → (s_Val s_x))) → (∀ s_x : Domain, ((s_V s_x) → (s_Val s_x)))
