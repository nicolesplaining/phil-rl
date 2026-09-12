import hashlib
import json
from pathlib import Path

from phil_rl.schema import Artifact
from phil_rl.verify import check


def test_research_archives_preserve_files_and_replay_checks():
    root = Path(__file__).parents[1] / "experiments"
    for manifest_path in root.glob("*/archive-manifest.json"):
        manifest = json.loads(manifest_path.read_text())
        for name, digest in manifest["sha256"].items():
            assert hashlib.sha256((manifest_path.parent / name).read_bytes()).hexdigest() == digest
        for path in manifest_path.parent.glob("*/argument.json"):
            artifact = Artifact.model_validate_json(path.read_text())
            expected = json.loads((path.parent / "checks.json").read_text())
            assert check(artifact)["status"] == expected["explicit"]["status"]
            assert check(artifact, True)["status"] == expected["with_proposed_implicit"]["status"]
