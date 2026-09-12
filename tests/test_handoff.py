import json

import pytest

from phil_rl.archive import archive_run
from phil_rl.audit import verify_run
from phil_rl.cli import save
from phil_rl.examples import fixtures
from phil_rl.source import GroundedReconstruction, source_units


def test_overlapping_duplicate_evidence_is_a_retriable_validation_error():
    source = "A. A. A."
    draft = GroundedReconstruction.model_validate(
        {
            "status": "argument",
            "reason": "",
            "title": "Repeated statements",
            "claims": [
                {
                    "id": f"c{i}",
                    "text": "A.",
                    "role": "conclusion" if i == 3 else "premise",
                    "origin": "explicit",
                    "evidence_ids": ids,
                    "interpretation_note": "",
                }
                for i, ids in [(1, ["s1"]), (2, ["s2", "s3"]), (3, ["s3"])]
            ],
            "relations": [{"premises": ["c1", "c2"], "conclusion": "c3", "kind": "supports"}],
            "conclusion_id": "c3",
            "ambiguities": [],
        }
    )
    with pytest.raises(ValueError, match="overlaps"):
        draft.materialize(source, source_units(source))


def test_verify_run_handles_a_single_artifact_and_missing_lean(tmp_path):
    directory = tmp_path / "source"
    save(directory, fixtures()["modus_ponens"][0], {"provenance": "test"})
    result = verify_run(directory, tmp_path / "checked", str(tmp_path / "missing-lean"))
    assert result["failures"] == 1 and result["proofs_checked"] == 0


def test_verify_run_does_not_invent_proofs_for_no_argument_outcomes(tmp_path):
    directory = tmp_path / "source"
    save(directory, None, {"outcome": "no_argument", "reason": "No inference."})
    result = verify_run(directory, tmp_path / "checked")
    assert result["cases"] == [] and result["proofs_checked"] == 0


def test_archive_preserves_files_and_refuses_overwrites_and_recursive_destinations(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "summary.json").write_text(json.dumps({"completed": 0}))
    with pytest.raises(ValueError, match="outside"):
        archive_run(source, source / "archive", "test")
    destination = tmp_path / "archive"
    archive_run(source, destination, "test")
    assert (source / "summary.json").read_bytes() == (destination / "summary.json").read_bytes()
    with pytest.raises(ValueError, match="already exists"):
        archive_run(source, destination, "test")
