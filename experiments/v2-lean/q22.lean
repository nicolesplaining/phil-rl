import Lean

-- Formalization SHA256: 9ec16ce9c53883a92f2b5fe7568dda8ce244843852939e8384cbd2bf5ab84c36
-- Reconstruction SHA256: d4b7489f385afe1c57943198c2b814f4b55ef60dc806cc49d375099e8e20985e
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.

theorem argumentProof (s_CriticSaysTrustworthy : Prop) (s_RecollectionFabricated : Prop) (s_RecollectionTrustworthy : Prop) :
    (s_RecollectionFabricated → (¬ s_RecollectionTrustworthy)) → s_RecollectionFabricated → (¬ s_RecollectionTrustworthy) := by
  classical
  by_cases h_CriticSaysTrustworthy : s_CriticSaysTrustworthy <;> by_cases h_RecollectionFabricated : s_RecollectionFabricated <;> by_cases h_RecollectionTrustworthy : s_RecollectionTrustworthy <;> simp_all

#print axioms argumentProof
