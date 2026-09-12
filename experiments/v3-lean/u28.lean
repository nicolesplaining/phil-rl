import Lean

-- Formalization SHA256: 29293c82d0494bd32e6246c71f30c592a68e6308a3fa6917037fd752ab877ad6
-- Reconstruction SHA256: 84e1c64049906a483f335c701a85c91a6dae1625c728706682f58e63d6d67193
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (Domain : Type) [Nonempty Domain] (s_Vera : Domain) (s_the_critic : Domain) (s_Thoughtful : Domain → Prop) : Prop :=
  (s_Vera = s_the_critic) → (s_Thoughtful s_the_critic) → (s_Thoughtful s_Vera)
