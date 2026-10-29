# API Reference

## Base URL

Local development: `http://127.0.0.1:8000`

Start the backend from the `backend` directory:

```powershell
python -m uvicorn app.main:app --reload
```

## Implemented endpoints

### `GET /health`

Checks whether the FastAPI application is responding.

Example:

```http
GET /health
```

Example response:

```json
{
  "status": "ok",
  "service": "proofpatch-api",
  "version": "0.1.0"
}
```

### Interactive documentation

When the backend is running, visit `/docs` for FastAPI's generated API documentation.

## Planned endpoint

A repair endpoint is not currently exposed by the FastAPI application. A future design may accept source code and tests and return:
- Baseline reproduction results.
- Model proposal and explanation.
- Patch validation results.
- Verification output and status.
- Relevant warnings and risks.

The request schema, authentication, limits, and response contract must be finalized before this endpoint is implemented. Do not treat this planned design as an available API.
