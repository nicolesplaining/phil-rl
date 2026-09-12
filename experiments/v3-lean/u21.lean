import Lean

-- Formalization SHA256: ea93e4c83d2b6654dc7ab2bebd7604f34398dffd972a100b0760223f59db0fc4
-- Reconstruction SHA256: 8921903442aacd33ed5fdf2480475656f8ec9f28a4c6145a9c337594432b098a
-- Includes proposed implicit premises: false
-- No claim of English fidelity or premise truth.

theorem argumentProof (s_PanelDiscussingEndorsement : Prop) (s_Coerced : Prop) (s_Voluntary : Prop) (s_Legitimate : Prop) :
    (s_Coerced → (¬ s_Voluntary)) → s_Coerced → ((¬ s_Voluntary) → (¬ s_Legitimate)) → (¬ s_Legitimate) := by
  classical
  by_cases h_PanelDiscussingEndorsement : s_PanelDiscussingEndorsement <;> by_cases h_Coerced : s_Coerced <;> by_cases h_Voluntary : s_Voluntary <;> by_cases h_Legitimate : s_Legitimate <;> simp_all

#print axioms argumentProof
