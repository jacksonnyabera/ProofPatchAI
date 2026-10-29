# ProofPatch AI

**Evidence-first AI-assisted bug repair.**

ProofPatch AI is a software repair project designed to reproduce a reported Python failure, request a minimal proposed patch from an AI model, validate the patch, and independently run the defined tests against the patched code.

The goal is to make repair decisions traceable to evidence rather than presenting an AI-generated suggestion as automatically correct.

## Current status

The project is under active development.

Implemented components include:
- Python bug reproduction using pytest in a temporary directory.
- Unified-diff validation and in-memory patch application.
- Evidence-informed repair prompts and model-response parsing.
- Independent verification against defined tests.
- An orchestration workflow that connects these steps.
- A FastAPI health endpoint.
- Automated tests for the repair components.

The HTTP API currently exposes `GET /health`. A public repair endpoint and end-to-end production integration are not yet implemented.

Live Meta model access depends on valid API credentials and account access. Mocked tests do not establish that a real Meta API request succeeds.

## How it works

1. Reproduce the reported failure with the supplied code and tests.
2. Stop if the baseline failure cannot be reproduced.
3. Ask the configured model client to propose a minimal patch using the supplied evidence.
4. Validate the unified diff and apply it in memory.
5. Run the defined tests against the patched code.
6. Return the observed result and evidence.

A passing test suite means the patch passed the tests that were run. It does not prove universal correctness or eliminate all security risks.

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

Create or update `backend/.env` using `backend/.env.example` as a reference. Never commit real credentials.

Current environment variable names:
- `MODEL_API_KEY`
- `META_MODEL`
- `META_API_BASE_URL`

Note: environment variables are documented for configuration, but not all are wired into the client and HTTP application yet. The current model client uses a hardcoded base URL.

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

## Frontend setup

In a separate terminal:

```powershell
cd frontend
npm ci
npm run dev
```

Open http://localhost:3000.

The frontend is an evolving part of the project; do not assume every repair workflow is connected to it yet.

## Security warning

The current Python reproduction and verification components execute code. Temporary directories are not a secure sandbox. Do not use this implementation to run untrusted code on a publicly accessible server.

Before public deployment, add process isolation, resource limits, network restrictions, authentication, rate limiting, and appropriate operational monitoring.

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
