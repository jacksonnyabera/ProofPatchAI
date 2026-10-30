# ProofPatch AI

**Evidence-first AI-assisted bug repair.**

ProofPatch AI reproduces a reported Python failure, requests a minimal proposed patch from an AI model, validates the patch, and independently runs defined tests against the patched code.

## Current status

Implemented components:
- Python bug reproduction using pytest in a temporary directory.
- Unified-diff validation and in-memory patch application.
- Evidence-informed repair prompts and model-response parsing.
- Independent verification against defined tests.
- Workflow orchestration.
- FastAPI health and local repair endpoints.
- Automated tests for repair components and API behavior.

### Available API endpoints

- `GET /health` — checks API availability.
- `POST /repair` — accepts Python source code and tests and invokes the repair workflow when explicitly enabled for trusted local development.

The repair endpoint is disabled by default. Its reproduction and verification stages execute supplied Python code without a secure sandbox. It is not safe for public use or untrusted submissions.

Live Meta model access remains unverified. Passing mocked tests does not establish that a real Meta API request succeeds.

## How it works

1. Reproduce the reported failure with the supplied code and tests.
2. Stop if the baseline failure cannot be reproduced.
3. Ask the configured model client to propose a minimal patch using the supplied evidence.
4. Validate the unified diff and apply it in memory.
5. Run the defined tests against the patched code.
6. Return the observed result and evidence.

Passing defined tests does not prove universal correctness.

## Technology

- Python
- FastAPI
- pytest
- httpx
- Next.js
- React
- TypeScript

## Requirements

- Python 3.13 is the current development environment.
- Node.js and npm are needed for frontend development.
- A valid model API key is needed only for a real model API request.

## Backend setup

From the repository root in PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create `backend/.env` using `backend/.env.example` as a reference. Never commit real credentials.

Configuration:
- `MODEL_API_KEY` — model API credential.
- `META_MODEL` — model name; defaults to `muse-spark-1.3`.
- `META_API_BASE_URL` — Meta API base URL; defaults to `https://api.meta.ai/v1`.
- `PROOFPATCH_ENABLE_LOCAL_REPAIR` — set to `true` only for trusted local testing; otherwise repair remains disabled.

The application reads environment variables from its process. To load `.env` when starting Uvicorn, use `--env-file .env`.

## Run the backend

From the `backend` directory:

```powershell
python -m uvicorn app.main:app --reload
```

Health check: http://127.0.0.1:8000/health

Interactive API documentation: http://127.0.0.1:8000/docs

## Run tests

From the `backend` directory:

```powershell
python -m pytest -q
```

The latest reported test run passed 28 tests.

## Frontend setup

In a separate terminal:

```powershell
cd frontend
npm ci
npm run dev
```

Open http://localhost:3000.

The frontend is not yet connected to the repair workflow.

## Security warning

The current Python reproduction and verification components execute code. Temporary directories are not a secure sandbox. Do not expose the repair endpoint publicly or enable it for untrusted submissions.

Before public deployment, add process isolation, resource limits, network restrictions, authentication, rate limiting, and operational monitoring.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [API](docs/API.md)
- [Security](docs/SECURITY.md)
- [Testing](docs/TESTING.md)
- [Contributing](docs/CONTRIBUTING.md)
- [Roadmap](docs/ROADMAP.md)

## Project principles

- Evidence before repair.
- Minimal, reviewable changes.
- Independent verification.
- Honest reporting of uncertainty and failures.
- No claim of correctness beyond the tests and checks actually performed.
