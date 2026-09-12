import os
import shutil

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
