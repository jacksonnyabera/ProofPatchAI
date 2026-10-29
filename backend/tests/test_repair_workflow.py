import json

from app.services.repair_workflow import run_repair_workflow


class FakeMetaClient:
    model = "mock-model"

    def __init__(self, patch):
        self.patch = patch

    def chat(self, prompt):
        return json.dumps({
            "root_cause": "Subtraction used instead of addition",
            "patch": self.patch,
            "explanation": "Use addition to fix the function.",
            "risks": [],
            "confidence": "high",
        })


def test_workflow_verifies_valid_repair():
    code = "def add(a, b):\n    return a - b\n"
    tests = "def test_add():\n    assert add(2, 3) == 5\n"
    patch = (
        "--- a/candidate.py\n"
        "+++ b/candidate.py\n"
        "@@ -1,2 +1,2 @@\n"
        " def add(a, b):\n"
        "-    return a - b\n"
        "+    return a + b\n"
    )

    result = run_repair_workflow(
        client=FakeMetaClient(patch),
        code=code,
        test_code=tests,
    )

    assert result["status"] == "verified_against_defined_tests"
    assert result["baseline"]["status"] == "failed"
    assert result["patch"]["valid"] is True
    assert result["verification"]["tests_passed"] is True
    assert result["verification"]["universal_correctness_proven"] is False


def test_workflow_rejects_invalid_patch():
    code = "def add(a, b):\n    return a - b\n"
    tests = "def test_add():\n    assert add(2, 3) == 5\n"

    result = run_repair_workflow(
        client=FakeMetaClient("not a valid unified diff"),
        code=code,
        test_code=tests,
    )

    assert result["status"] == "patch_rejected"
    assert result["patch"]["valid"] is False
    assert result["verification"] is None


def test_workflow_stops_when_baseline_passes():
    code = "def add(a, b):\n    return a + b\n"
    tests = "def test_add():\n    assert add(2, 3) == 5\n"

    class UnexpectedClient:
        model = "mock-model"

        def chat(self, prompt):
            raise AssertionError("Model must not be called")

    result = run_repair_workflow(
        client=UnexpectedClient(),
        code=code,
        test_code=tests,
    )

    assert result["status"] == "baseline_not_reproduced"
    assert result["baseline"]["status"] == "passed"
    assert result["proposal"] is None
