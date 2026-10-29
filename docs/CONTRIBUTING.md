# Contributing

Thanks for your interest in ProofPatch AI.

## Development principles

- Keep changes small and reviewable.
- Preserve evidence from baseline and verification runs.
- Prefer explicit failure statuses over silent fallbacks.
- Do not claim a patch is correct beyond the checks performed.
- Keep secrets out of source control.
- Do not weaken tests merely to make a change pass.

## Local setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
```

## Suggested workflow

1. Create a focused branch.
2. Make a small change.
3. Add or update tests for the behavior.
4. Run the relevant test module.
5. Run the complete backend test suite.
6. Review `git diff` for unintended changes or secrets.
7. Document limitations and any security implications.
8. Open a pull request with a concise summary and test results.

## Pull request checklist

- [ ] The change has a clear purpose.
- [ ] Tests cover the relevant behavior.
- [ ] Existing tests still pass.
- [ ] No real credentials or private data are included.
- [ ] Documentation is updated where needed.
- [ ] Claims about verification accurately describe what was tested.

## Scope

The project is evolving. Discuss substantial architecture changes before introducing new frameworks or replacing working components.
