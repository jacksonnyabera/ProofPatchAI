# Architecture

## Overview

ProofPatch AI separates the repair process into components so each stage can be tested independently.

```text
Input source code + tests
          |
          v
Bug reproducer
          |
          v
Baseline failure report
          |
          v
Repair prompt and model client
          |
          v
Structured repair proposal
          |
          v
Unified-diff validation
          |
          v
In-memory patch application
          |
          v
Independent verification
          |
          v
Evidence-based workflow result
```

## Components

### `app/main.py`
Creates the FastAPI application and currently exposes `GET /health`.

### `app/services/bug_reproducer.py`
Runs the supplied Python code and tests in a temporary directory and captures the execution outcome. Execution has a timeout, but this is not a security sandbox.

### `app/services/repair_prompt.py`
Builds a prompt that supplies the code, tests, and baseline evidence. The prompt treats supplied content as untrusted input and asks for a structured response.

### `app/services/repair_service.py`
Requests a proposal from the provided model client and parses the response into fields such as root cause, patch, explanation, risks, and confidence. A proposal is not itself verification.

### `app/services/patch_engine.py`
Validates and applies a supported unified diff in memory. It is intended to avoid modifying the original project files during patch application.

### `app/services/verify_repair.py`
Runs the defined tests against the candidate patched code and reports whether verification passed, failed, or timed out.

### `app/services/repair_workflow.py`
Coordinates baseline reproduction, proposal generation, patch validation, and verification. It stops early when the baseline failure cannot be reproduced or the patch is rejected.

### `meta_client.py`
Contains the HTTP client used to request model completions. Real API use requires valid credentials and a compatible endpoint/model configuration.

## Workflow statuses

Statuses communicate what happened at a particular stage. Examples include:
- `baseline_timeout`: the initial reproduction exceeded its time limit.
- `baseline_not_reproduced`: the initial failure was not reproduced.
- `patch_rejected`: the proposed diff was invalid or could not be applied.
- `verification_failed`: the candidate did not pass verification.
- `verification_timeout`: verification exceeded its time limit.
- `verified_against_defined_tests`: the candidate passed the tests that were run.

A status is not a claim that all possible bugs are fixed.

## Current boundary

The orchestration service exists as Python code, but the HTTP application currently exposes only the health route. A public repair endpoint, frontend integration, and secure execution isolation remain future work.
