import Lean

-- Formalization SHA256: faeec27db54d2f6890d429d7fa6eba7496c33d4349632b2f72beb9f84947a65a
-- Reconstruction SHA256: 93a7d71257cfa7a938fc9f486feb6130c8cf71c570e0b0229937fbed87ebece6
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_V : Prop) (s_S : Prop) : Prop :=
  (s_V ↔ s_S) → s_S → s_V
