from fastapi import FastAPI

app = FastAPI(
    title="ProofPatch AI",
    description="Evidence-based AI software repair agent",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "proofpatch-api",
        "version": "0.1.0",
    }