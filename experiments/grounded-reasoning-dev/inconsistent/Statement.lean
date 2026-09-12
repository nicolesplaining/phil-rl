import Lean

-- Formalization SHA256: d507a709802abdc1746e253e7c3af12cb9ff28f62ba292fb389750a37c07965a
-- Reconstruction SHA256: 82c25783c5fcb5ca8d038f286862265096f96ea83d0c402182278aa77f5833b6
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.
-- This definition is a statement, NOT a proof.
def argumentStatement (s_R : Prop) (s_F : Prop) : Prop :=
  s_R → (¬ s_R) → s_F
