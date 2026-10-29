
import pytest

from app.services.verify_repair import verify_repair


def test_verifier_accepts_patch_when_original_test_passes():
    original = "def add(a, b):\n    return a - b\n"
    patched = "def add(a, b):\n    return a + b\n"
    test_code = "def test_add():\n    assert add(2, 3) == 5\n"

    result = verify_repair(
        original_code=original,
        patched_code=patched,
        test_code=test_code,
        baseline_report={"status": "failed"},
    )

    assert result["status"] == "verified_against_defined_tests"
    assert result["tests_passed"] is True
    assert result["universal_correctness_proven"] is False


def test_verifier_reports_failure_when_patch_is_wrong():
    original = "def add(a, b):\n    return a - b\n"
    patched = "def add(a, b):\n    return a * b\n"
    test_code = "def test_add():\n    assert add(2, 3) == 5\n"

    result = verify_repair(
        original_code=original,
        patched_code=patched,
        test_code=test_code,
        baseline_report={"status": "failed"},
    )

    assert result["status"] == "verification_failed"
    assert result["tests_passed"] is False


def test_verifier_rejects_unreproduced_baseline():
    with pytest.raises(ValueError, match="baseline failure"):
        verify_repair(
            original_code="def add(a, b):\n    return a - b\n",
            patched_code="def add(a, b):\n    return a + b\n",
            test_code="def test_add():\n    assert add(2, 3) == 5\n",
            baseline_report={"status": "passed"},
        )
