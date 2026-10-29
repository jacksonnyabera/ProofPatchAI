
import pytest

from app.services.repair_prompt import build_repair_prompt


def test_prompt_includes_code_tests_and_failure_evidence():
    report = {
        "status": "failed",
        "exit_code": 1,
        "command": "python -m pytest -q",
        "stdout": "assert -1 == 5",
        "stderr": "",
    }

    prompt = build_repair_prompt(
        code="def add(a, b):\n    return a - b\n",
        test_code="def test_add():\n    assert add(2, 3) == 5\n",
        baseline_report=report,
    )

    assert "def add(a, b):" in prompt
    assert "def test_add():" in prompt
    assert "assert -1 == 5" in prompt
    assert "Do not claim that the repair has passed tests." in prompt


def test_prompt_rejects_passing_baseline():
    with pytest.raises(ValueError, match="reproduced baseline failure"):
        build_repair_prompt(
            code="def add(a, b):\n    return a + b\n",
            test_code="def test_add():\n    assert add(2, 3) == 5\n",
            baseline_report={"status": "passed"},
        )
