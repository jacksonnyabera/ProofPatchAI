# Testing Guide

## Backend tests

Activate the backend virtual environment and install dependencies:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run all tests:

```powershell
python -m pytest -q
```

Run one test module:

```powershell
python -m pytest tests/test_repair_workflow.py -q
```

## What the tests should cover

- Health endpoint response.
- Baseline failure reproduction and timeout handling.
- Unified-diff acceptance and rejection.
- Repair prompt content and treatment of untrusted input.
- Model-response parsing and invalid responses.
- Verification pass, failure, and timeout behavior.
- Workflow early exits, rejected patches, and successful verification.

## Model API tests

Unit tests should use a fake or mocked client so that normal test runs do not require a real API key, incur API costs, or depend on network availability.

A mocked test only verifies the behavior represented by the mock. It does not prove that the live Meta endpoint, model name, credentials, or billing configuration work.

Run live integration tests separately and only when credentials and account access are available. Never print or commit the key.

## Interpreting results

A passing test suite means the tests completed successfully. It does not prove universal correctness, safety, or compatibility with all repositories.

When a test fails, preserve the failure output and fix the underlying issue before changing expected behavior.
