"""Preserve measured results, including model failures; this is not a fidelity score."""

import json
from pathlib import Path

import pytest

from phil_rl.schema import Artifact
from phil_rl.verify import check

ARCHIVE = Path(__file__).parents[1] / "experiments" / "initial"


@pytest.mark.parametrize("path", sorted(ARCHIVE.rglob("argument.json")))
def test_archived_results_remain_replayable(path):
    artifact = Artifact.model_validate_json(path.read_text())
    recorded = json.loads(path.with_name("checks.json").read_text())
    assert check(artifact)["status"] == recorded["explicit"]["status"]
    assert check(artifact, True)["status"] == recorded["with_proposed_implicit"]["status"]
