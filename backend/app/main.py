import logging
import os
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.services.repair_workflow import run_repair_workflow
from meta_client import MetaModelClient

logger = logging.getLogger(__name__)

app = FastAPI(
    title="ProofPatch AI",
    description="Evidence-based AI software repair agent",
    version="0.1.0",
)


class RepairRequest(BaseModel):
    code: str = Field(min_length=1, max_length=20_000)
    test_code: str = Field(min_length=1, max_length=20_000)


class RepairResponse(BaseModel):
    status: str
    baseline: dict[str, Any]
    proposal: dict[str, Any] | None
    patch: dict[str, Any] | None
    verification: dict[str, Any] | None


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "proofpatch-api",
        "version": "0.1.0",
    }


@app.post("/repair", response_model=RepairResponse)
def repair(request: RepairRequest):
    # This workflow executes supplied Python code.
    # It must remain disabled unless explicitly enabled for trusted local testing.
    if os.getenv("PROOFPATCH_ENABLE_LOCAL_REPAIR", "").lower() != "true":
        raise HTTPException(
            status_code=503,
            detail="Repair endpoint is disabled. Enable only for trusted local development.",
        )

    if not request.code.strip() or not request.test_code.strip():
        raise HTTPException(
            status_code=422,
            detail="Code and test_code must contain non-whitespace text.",
        )

    api_key = os.getenv("MODEL_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="Model API credentials are not configured.",
        )

    client = None

    try:
        client = MetaModelClient(
            api_key=api_key,
            model=os.getenv("META_MODEL", "muse-spark-1.3"),
        )

        return run_repair_workflow(
            client=client,
            code=request.code,
            test_code=request.test_code,
        )

    except Exception as exc:
        logger.exception("Repair workflow failed")
        raise HTTPException(
            status_code=502,
            detail="Repair workflow failed. Check server logs.",
        ) from exc

    finally:
        if client is not None:
            client.close()
