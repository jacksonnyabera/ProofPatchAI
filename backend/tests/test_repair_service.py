
import json

import pytest

from app.services.repair_service import propose_repair


class FakeMetaClient:
    model = "muse-spark-1.3"

    def __init__(self, response):
        self.response = response
        self.last_prompt = None

    def chat(self, prompt):
        self.last_prompt = prompt
        return self.response


def test_propose_repair_returns_unverified_proposal():
    response = {
        "root_cause": "Subtraction used instead of addition",
        "patch": "--- a/candidate.py\n+++ b/candidate.py\n",
        "explanation": "Use addition for this function",
        "risks": [],
        "confidence": "high",
    }
    client = FakeMetaClient(json.dumps(response))

    result = propose_repair(
        client=client,
        code="def add(a, b):\n    return a - b\n",
        test_code="def test_add():\n    assert add(2, 3) == 5\n",
        baseline_report={
            "status": "failed",
            "exit_code": 1,
            "stdout": "assert -1 == 5",
            "stderr": "",
        },
    )

    assert result["status"] == "proposal_only"
    assert result["model"] == "muse-spark-1.3"
    assert result["verified"] is False
    assert result["proposal"]["root_cause"] == response["root_cause"]
    assert "assert -1 == 5" in client.last_prompt


def test_propose_repair_rejects_invalid_json():
    client = FakeMetaClient("not JSON")

    with pytest.raises(ValueError, match="invalid JSON"):
        propose_repair(
            client=client,
            code="def add(a, b):\n    return a - b\n",
            test_code="def test_add():\n    assert add(2, 3) == 5\n",
            baseline_report={"status": "failed", "exit_code": 1},
        )


def test_propose_repair_rejects_passing_baseline():
    client = FakeMetaClient("{}")

    with pytest.raises(ValueError, match="reproduced baseline failure"):
        propose_repair(
            client=client,
            code="def add(a, b):\n    return a + b\n",
            test_code="def test_add():\n    assert add(2, 3) == 5\n",
            baseline_report={"status": "passed"},
        )
