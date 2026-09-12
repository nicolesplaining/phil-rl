"""Reproducible review records and independent Lean checks for saved runs."""

import json
from pathlib import Path

from phil_rl.benchmark import load_suite, reference
from phil_rl.fidelity import MeaningReview, assess
from phil_rl.schema import Artifact, fingerprint


def audit_run(run_directory: Path, decisions_path: Path, destination: Path):
    from phil_rl.cli import write_json

    suite = load_suite(run_directory / "suite.json")
    decisions = json.loads(decisions_path.read_text())
    expected_ids = {c["id"] for c in suite["cases"]}
    if set(decisions["cases"]) != expected_ids:
        raise ValueError("Record a decision for every case, including failures.")
    destination.mkdir(parents=True, exist_ok=False)
    write_json(destination / "decisions.json", decisions)
    rows = []
    for case in suite["cases"]:
        decision = decisions["cases"][case["id"]]
        directory = run_directory / case["id"]
        ref = reference(case)
        row = {
            "case": case["id"],
            "supported": ref is not None,
            "passed": False,
            "review_notes": decision["notes"],
        }
        argument_path = directory / "argument.json"
        if not (directory / "checks.json").exists():
            row["reason"] = "Generation failed or result is missing."
        elif not decision.get("approved", False):
            row["reason"] = decision.get("category", "Source interpretation not approved.")
        elif ref is None:
            checks = json.loads((directory / "checks.json").read_text())
            if case["status"] == "review_required":
                generated = (
                    Artifact.model_validate_json(argument_path.read_text())
                    if argument_path.exists()
                    else None
                )
                row["passed"] = bool(generated and generated.reconstruction.ambiguities)
            else:
                row["passed"] = checks["explicit"]["status"] == case["status"]
            row["method"] = "agent-reviewed source outcome, not formula equivalence"
        elif argument_path.exists():
            generated = Artifact.model_validate_json(argument_path.read_text())
            groups = decision.get("claims")
            if groups is None:
                groups = [
                    {
                        "reference_ids": [c.id],
                        "generated_ids": [
                            g.id
                            for g in generated.reconstruction.claims
                            if g.origin == "explicit"
                            and g.role == c.role
                            and g.evidence == c.evidence
                        ],
                    }
                    for c in ref.reconstruction.claims
                ]
            try:
                review = MeaningReview(
                    reference_sha256=fingerprint(ref),
                    generated_sha256=fingerprint(generated),
                    reviewer_kind=decisions["reviewer_kind"],
                    symbol_map=decision["symbol_map"],
                    glossary_rationale=decision["notes"],
                    claims=groups,
                    source_meaning_approved=True,
                    source_review_notes=decision["notes"],
                    domain_restriction=decision.get("domain_restriction"),
                )
                result = assess(ref, generated, review)
                write_json(destination / (case["id"] + "-alignment.json"), review.model_dump())
                write_json(destination / (case["id"] + "-comparison.json"), result)
                row["passed"] = result["status"] == "passed_under_reviewed_alignment"
                row["comparison"] = result["status"]
            except ValueError as error:
                row["reason"] = str(error)
        rows.append(row)
    supported = [r for r in rows if r["supported"]]
    other = [r for r in rows if not r["supported"]]
    result = {
        "suite_sha256": fingerprint(suite),
        "reviewer_kind": decisions["reviewer_kind"],
        "supported_total": len(supported),
        "supported_passed": sum(r["passed"] for r in supported),
        "other_total": len(other),
        "other_passed": sum(r["passed"] for r in other),
        "cases": rows,
        "qualification": "Agent-authored references and glossary review, not human validation.",
    }
    write_json(destination / "summary.json", result)
    return result


def verify_run(run_directory: Path, destination: Path, lean_bin="lean"):
    from phil_rl.cli import write_json
    from phil_rl.lean import check_lean, export
    from phil_rl.verify import check

    destination.mkdir(parents=True, exist_ok=False)
    rows = []
    for path in sorted(run_directory.glob("*/argument.json")):
        artifact = Artifact.model_validate_json(path.read_text())
        diagnostic = check(artifact)
        row = {"case": path.parent.name, "encoding_status": diagnostic["status"]}
        if diagnostic["status"] == "unsupported":
            row["lean"] = {"status": "not_applicable", "proof_checked": False}
        else:
            prove = (
                diagnostic["status"] == "valid"
                and artifact.formalization.logic == "classical_propositional"
            )
            code = export(artifact, prove=prove)
            (destination / (path.parent.name + ".lean")).write_text(code)
            row["lean"] = check_lean(code, lean_bin)
            row["requested_proof"] = prove
        rows.append(row)
        result = {
            "cases": rows,
            "proofs_checked": sum(bool(r["lean"].get("proof_checked")) for r in rows),
            "failures": sum(r["lean"]["status"] not in {"passed", "not_applicable"} for r in rows),
            "note": "First-order exports are statements, not kernel-checked proofs.",
        }
        write_json(destination / "summary.json", result)
    return result
