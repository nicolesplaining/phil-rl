import json
import os
import shutil
from pathlib import Path

import pytest

from phil_rl.examples import fixtures
from phil_rl.lean import check_lean, export

LEAN = os.environ.get("LEAN_BIN", shutil.which("lean"))
pytestmark = pytest.mark.skipif(
    not LEAN, reason="Set LEAN_BIN or install the pinned Lean toolchain."
)


@pytest.mark.parametrize(
    "name", ["modus_ponens", "affirming_consequent", "missing_bridge", "syllogism", "scope"]
)
def test_statements_typecheck_without_claiming_proofs(name):
    result = check_lean(export(fixtures()[name][0]), LEAN)
    assert result["status"] == "passed", result
    assert result["statement_typechecked"]
    assert not result["proof_checked"]


@pytest.mark.parametrize(
    "name,implicit", [("modus_ponens", False), ("missing_bridge", True), ("circular", False)]
)
def test_actual_lean_kernel_checks(name, implicit):
    result = check_lean(export(fixtures()[name][0], implicit, prove=True), LEAN)
    assert result["proof_checked"], result
    assert "sorryAx" not in result["stdout"]


FINAL_EXPORTS = Path(__file__).parents[1] / "experiments" / "v3-lean"
FINAL_CASES = [
    case
    for case in json.loads((FINAL_EXPORTS / "summary.json").read_text())["cases"]
    if case["lean"]["status"] == "passed"
]


@pytest.mark.parametrize("case", FINAL_CASES, ids=lambda case: case["case"])
def test_final_run_exports_replay_in_the_kernel(case):
    code = (FINAL_EXPORTS / (case["case"] + ".lean")).read_text()
    result = check_lean(code, LEAN)
    assert result["status"] == "passed", result
    assert result["proof_checked"] == case["lean"]["proof_checked"]
