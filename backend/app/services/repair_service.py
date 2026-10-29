
import json
from typing import Any

from app.services.repair_prompt import build_repair_prompt
from meta_client import MetaModelClient


def propose_repair(
    client: MetaModelClient,
    code: str,
    test_code: str,
    baseline_report: dict[str, Any],
) -> dict[str, Any]:
    """Ask Meta for a repair proposal based on reproduced failure evidence.

    This function proposes a patch only. It does not apply or verify it.
    """
    prompt = build_repair_prompt(
        code=code,
        test_code=test_code,
        baseline_report=baseline_report,
    )

    raw_response = client.chat(prompt)

    try:
        proposal = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise ValueError("Meta returned invalid JSON for the repair proposal") from exc

    required_fields = {
        "root_cause",
        "patch",
        "explanation",
        "risks",
        "confidence",
    }

    if not isinstance(proposal, dict) or not required_fields.issubset(proposal):
        raise ValueError("Meta response is missing required repair proposal fields")

    if not isinstance(proposal["risks"], list):
        raise ValueError("Repair proposal risks must be a list")

    if proposal["confidence"] not in {"low", "medium", "high"}:
        raise ValueError("Repair proposal confidence is invalid")

    return {
        "status": "proposal_only",
        "model": client.model,
        "proposal": proposal,
        "verified": False,
    }
