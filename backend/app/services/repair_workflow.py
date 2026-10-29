from typing import Any

from app.services.bug_reproducer import reproduce_python_bug
from app.services.patch_engine import apply_unified_diff
from app.services.repair_service import propose_repair
from app.services.verify_repair import verify_repair


def run_repair_workflow(
    client: Any,
    code: str,
    test_code: str,
) -> dict[str, Any]:
    """Run the evidence-first repair workflow without modifying project files."""

    baseline = reproduce_python_bug(
        code=code,
        test_code=test_code,
    )

    if baseline["status"] != "failed":
        return {
            "status": (
                "baseline_timeout"
                if baseline["status"] == "timeout"
                else "baseline_not_reproduced"
            ),
            "baseline": baseline,
            "proposal": None,
            "patch": None,
            "verification": None,
        }

    proposal_result = propose_repair(
        client=client,
        code=code,
        test_code=test_code,
        baseline_report=baseline,
    )
    proposal = proposal_result["proposal"]

    patch_result = apply_unified_diff(
        original_code=code,
        patch=proposal["patch"],
        target_filename="candidate.py",
    )

    if not patch_result.valid:
        return {
            "status": "patch_rejected",
            "baseline": baseline,
            "proposal": proposal_result,
            "patch": {
                "valid": False,
                "error": patch_result.error,
            },
            "verification": None,
        }

    verification = verify_repair(
        original_code=code,
        patched_code=patch_result.patched_code,
        test_code=test_code,
        baseline_report=baseline,
    )

    return {
        "status": verification["status"],
        "baseline": baseline,
        "proposal": proposal_result,
        "patch": {
            "valid": True,
            "target_filename": "candidate.py",
            "patched_code": patch_result.patched_code,
        },
        "verification": verification,
    }
