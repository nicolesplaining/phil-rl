import Lean

-- Formalization SHA256: 4d12f0336fec6a95616ce46b036bbf3817a84bfc598398cdb72c82968c315cef
-- Reconstruction SHA256: 2639707b1115f4cf0400f4366c729a40147a4942e17b50ae58a797fa845399ba
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Promise : Domain → Prop) (s_Commitment : Domain → Prop) (s_Sensation : Domain → Prop) : Prop :=
  (∀ s_x : Domain, ((s_Promise s_x) → (s_Commitment s_x))) → (∀ s_x : Domain, ((s_Commitment s_x) → (¬ (s_Sensation s_x)))) → (∀ s_x : Domain, ((s_Promise s_x) → (¬ (s_Sensation s_x))))
