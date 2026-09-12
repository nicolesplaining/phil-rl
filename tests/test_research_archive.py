import hashlib
import json
from pathlib import Path

from phil_rl.audit import audit_run
from phil_rl.schema import Artifact
from phil_rl.verify import check


def test_research_archives_preserve_files_and_replay_checks():
    root = Path(__file__).parents[1] / "experiments"
    for manifest_path in root.glob("*/archive-manifest.json"):
        manifest = json.loads(manifest_path.read_text())
        for name, digest in manifest["sha256"].items():
            assert hashlib.sha256((manifest_path.parent / name).read_bytes()).hexdigest() == digest
        for path in manifest_path.parent.rglob("argument.json"):
            artifact = Artifact.model_validate_json(path.read_text())
            expected = json.loads((path.parent / "checks.json").read_text())
            assert check(artifact)["status"] == expected["explicit"]["status"]
            assert check(artifact, True)["status"] == expected["with_proposed_implicit"]["status"]


def test_final_reviewed_comparisons_replay_without_model_calls(tmp_path):
    root = Path(__file__).parents[1] / "experiments"
    result = audit_run(
        root / "heldout-v3", root / "reviews" / "v3-decisions.json", tmp_path / "audit"
    )
    assert result["supported_passed"] == 31 and result["supported_total"] == 32
    assert result["other_passed"] == result["other_total"] == 8
    assert [row["case"] for row in result["cases"] if not row["passed"]] == ["u15"]
