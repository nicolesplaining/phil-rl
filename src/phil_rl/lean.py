"""Deterministic Lean export. Defining a proposition does not prove it."""

import subprocess
import tempfile
from pathlib import Path

from phil_rl.logic import parse, to_lean
from phil_rl.schema import Artifact
from phil_rl.verify import check


def export(artifact: Artifact, include_implicit: bool = False, prove: bool = False) -> str:
    artifact = Artifact.model_validate(artifact.model_dump())
    formalization = artifact.formalization
    ids = artifact.reconstruction.premise_ids(include_implicit)
    ids.append(artifact.reconstruction.conclusion_id)
    formulas = {t.claim_id: t.formula for t in formalization.translations}
    if formalization.logic == "unsupported" or any(formulas[c] is None for c in ids):
        raise ValueError("Cannot export unsupported active claims.")
    parameters = []
    if formalization.logic == "classical_first_order":
        parameters.extend(["(Domain : Type)", "[Nonempty Domain]"])
    for symbol in formalization.symbols:
        if symbol.kind == "proposition":
            kind = "Prop"
        elif symbol.kind == "constant":
            kind = "Domain"
        else:
            kind = " → ".join(["Domain"] * symbol.arity + ["Prop"])
        parameters.append(f"(s_{symbol.name} : {kind})")
    statement = " → ".join(to_lean(parse(formulas[c])) for c in ids)
    preamble = (
        "import Lean\n\n"
        f"-- Formalization SHA256: {artifact.formalization_sha256}\n"
        f"-- Reconstruction SHA256: {artifact.reconstruction_sha256}\n"
        f"-- Includes proposed implicit premises: {str(include_implicit).lower()}\n"
        "-- No claim of English fidelity or premise truth.\n"
    )
    binders = " ".join(parameters)
    if not prove:
        return preamble + (
            "-- This definition is a statement, NOT a proof.\n"
            f"def argumentStatement {binders} : Prop :=\n  {statement}\n"
        )
    if formalization.logic != "classical_propositional" or len(formalization.symbols) > 8:
        raise ValueError("Automatic Lean proof generation supports at most 8 proposition symbols.")
    if check(artifact, include_implicit)["status"] != "valid":
        raise ValueError("Refusing to prove an invalid, inconsistent, or undecided argument.")
    lines = [preamble, f"theorem argumentProof {binders} :\n    {statement} := by", "  classical"]
    # Case splitting is deliberately small and deterministic, then Lean checks the proof term.
    if formalization.symbols:
        tactics = [f"by_cases h_{s.name} : s_{s.name}" for s in formalization.symbols]
        lines.append("  " + " <;> ".join(tactics + ["simp_all"]))
    else:
        lines.append("  simp_all")
    lines.append("\n#print axioms argumentProof")
    return "\n".join(lines) + "\n"


def check_lean(code: str, executable: str = "lean", timeout: int = 60) -> dict:
    """Only pass compiler-produced code here, never an LLM-produced Lean program."""
    with tempfile.TemporaryDirectory(prefix="phil-lean-") as directory:
        path = Path(directory) / "Argument.lean"
        path.write_text(code)
        try:
            result = subprocess.run(
                [executable, str(path)],
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except FileNotFoundError:
            return {"status": "unavailable", "reason": "Lean executable not found."}
        except subprocess.TimeoutExpired:
            return {"status": "timeout"}
        proof = "theorem argumentProof" in code
        has_sorry = "sorryAx" in result.stdout or "sorry" in result.stderr
        passed = result.returncode == 0 and not has_sorry
        return {
            "status": "passed" if passed else "failed",
            "statement_typechecked": passed,
            "proof_checked": passed and proof,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
