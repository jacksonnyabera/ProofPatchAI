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

Example response:

```json
{
  "status": "ok",
  "service": "proofpatch-api",
  "version": "0.1.0"
}
```

### `POST /repair`

Accepts Python source code and test code and runs the evidence-first repair workflow.

**Safety:** This endpoint is disabled by default. It executes supplied Python code during reproduction and verification. It is intended only for trusted local development and is not safe for public or untrusted submissions.

#### Enablement

The backend process requires:

```text
PROOFPATCH_ENABLE_LOCAL_REPAIR=true
MODEL_API_KEY=<your model API key>
```

Do not commit credentials or expose this endpoint to untrusted users.

#### Request body

Content type: `application/json`

```json
{
  "code": "def add(a, b):\n    return a - b\n",
  "test_code": "def test_add():\n    assert add(2, 3) == 5\n"
}
```

| Field | Type | Requirements |
|---|---|---|
| `code` | string | Required; 1–20,000 characters |
| `test_code` | string | Required; 1–20,000 characters |

Whitespace-only code or test content is rejected when the endpoint is enabled.

#### Workflow behavior

1. Runs the supplied tests against the original code.
2. Stops if the baseline failure is not reproduced.
3. Requests a repair proposal from the configured model.
4. Validates and applies the proposed unified diff in memory.
5. Runs the supplied tests against the patched code.
6. Returns the workflow result and captured evidence.

The endpoint does not modify the user's original project files.

#### Response structure

The JSON response contains:
- `status` — overall workflow outcome.
- `baseline` — original test execution result and evidence.
- `proposal` — model proposal details, or `null` if no proposal was produced.
- `patch` — patch validation result and patched code, or `null`.
- `verification` — post-patch test result, or `null` if verification was not reached.

Possible workflow statuses include:
- `baseline_not_reproduced`
- `baseline_timeout`
- `patch_rejected`
- `verified_against_defined_tests`
- `verification_failed`
- `verification_timeout`

`verified_against_defined_tests` means only that the defined tests passed. It does not prove universal correctness.

#### HTTP errors

| HTTP status | Meaning |
|---|---|
| `422` | Invalid request fields or whitespace-only code/test content |
| `503` | Repair endpoint is disabled or model credentials are missing |
| `502` | Repair workflow or model request failed |

Internal exception details are logged by the backend and are not returned to the API caller.

## Interactive documentation

When the backend is running, visit `/docs` for FastAPI's generated API documentation.

## Current limitations

- The repair endpoint is disabled by default.
- Code execution is not isolated in a secure sandbox.
- Authentication and rate limiting are not implemented.
- The model name and API base URL are configurable through `META_MODEL` and `META_API_BASE_URL`.
- Live Meta API integration has not yet been verified.
- The frontend is not yet connected to the repair workflow.
