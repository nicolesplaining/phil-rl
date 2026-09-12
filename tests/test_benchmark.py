from pathlib import Path

from phil_rl.benchmark import load_suite, reference
from phil_rl.verify import check


def test_frozen_suite_references_are_well_formed_and_have_expected_status():
    suite = load_suite(Path(__file__).parents[1] / "benchmarks" / "heldout-v1.json")
    assert len(suite["cases"]) >= 40
    for case in suite["cases"]:
        artifact = reference(case)
        if artifact:
            assert check(artifact)["status"] == case["status"], case["id"]
