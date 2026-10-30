# Roadmap

This roadmap describes planned work and current implementation status. Priorities may change as the project develops.

## Phase 1 — Core repair workflow

- [x] Baseline reproduction component.
- [x] Unified-diff patch validation and in-memory application.
- [x] Evidence-informed repair prompt.
- [x] Independent defined-test verification.
- [x] Workflow orchestration and unit tests.
- [x] FastAPI health endpoint.
- [x] Initial edge-case handling and validation based on tests.

## Phase 2 — Model integration

- [ ] Resolve Meta API account, billing, and credential access.
- [ ] Make model base URL and model selection consistently configurable.
- [ ] Add safe, mocked client tests for API errors and malformed responses.
- [ ] Perform a real integration test when access is available.
- [ ] Document supported model and endpoint behavior based on verified requests.

## Phase 3 — API contract

- [x] Define the initial repair request and response schema.
- [x] Add a repair endpoint that invokes the workflow.
- [x] Add initial request validation, field-size limits, error handling, and workflow status reporting.
- [x] Add API endpoint tests.
- [ ] Add authentication and rate limiting before any public exposure.
- [ ] Version the API contract before a stable public release.

## Phase 4 — Execution isolation

- [ ] Implement isolated execution for untrusted code.
- [ ] Restrict network and filesystem access.
- [ ] Enforce CPU, memory, process, disk, and time limits.
- [ ] Add cleanup and operational monitoring.

## Phase 5 — Frontend integration

- [ ] Connect the frontend to implemented backend endpoints.
- [ ] Display baseline evidence, proposed diff, and verification results.
- [ ] Make failed, timed-out, and verified-against-tests outcomes visually distinct.
- [ ] Allow users to inspect and approve changes before applying them to a real repository.

## Phase 6 — Release readiness

- [ ] Add end-to-end tests.
- [ ] Document deployment and environment configuration.
- [ ] Add logging that avoids secrets and sensitive source content.
- [ ] Review security, privacy, reliability, and cost controls.
- [ ] Publish only claims supported by demonstrated functionality.

## Definition of done

A feature is complete when its behavior is implemented, tested, documented, and its limitations are clear. A mocked integration is not considered a successful live integration.
