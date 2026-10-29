
from typing import Any

from app.services.bug_reproducer import reproduce_python_bug


def verify_repair(
    original_code: str,
    patched_code: str,
    test_code: str,
    baseline_report: dict[str, Any],
) -> dict[str, Any]:
    """Test proposed replacement code against the same test suite.

    A passing result means only that the supplied tests passed.
    It does not prove the patch is universally correct or safe.
    """
    if baseline_report.get("status") != "failed":
        raise ValueError(
            "A reproduced baseline failure is required before verification"
        )

    if not original_code.strip():
        raise ValueError("Original code cannot be empty")

    if not patched_code.strip():
        raise ValueError("Patched code cannot be empty")

    if patched_code == original_code:
        raise ValueError("Patched code must differ from original code")

    result = reproduce_python_bug(
        code=patched_code,
        test_code=test_code,
    )

    if result["status"] == "passed":
        status = "verified_against_defined_tests"
    elif result["status"] == "timeout":
        status = "verification_timeout"
    else:
        status = "verification_failed"

    return {
        "status": status,
        "baseline_status": baseline_report["status"],
        "patched_test_status": result["status"],
        "patched_exit_code": result["exit_code"],
        "patched_stdout": result["stdout"],
        "patched_stderr": result["stderr"],
        "tests_passed": result["status"] == "passed",
        "universal_correctness_proven": False,
    }
