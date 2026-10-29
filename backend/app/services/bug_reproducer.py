import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


def reproduce_python_bug(
    code: str,
    test_code: str,
    timeout_seconds: int = 5,
) -> dict[str, Any]:
    """Run a supplied Python snippet and tests in a temporary directory.

    Captures the baseline test result before any patch is attempted.
    This is a prototype, not a secure sandbox for untrusted code.
    """
    if not code.strip():
        raise ValueError("Python code cannot be empty")

    if not test_code.strip():
        raise ValueError("Test code cannot be empty")

    if not 1 <= timeout_seconds <= 30:
        raise ValueError("timeout_seconds must be between 1 and 30")

    with tempfile.TemporaryDirectory(prefix="proofpatch-") as temp_dir:
        workspace = Path(temp_dir)
        source_file = workspace / "candidate.py"
        test_file = workspace / "test_candidate.py"

        test_code = (
            "import sys\n"
            f"sys.path.insert(0, {str(workspace)!r})\n"
            "from candidate import *\n\n"
            + test_code
        )

        source_file.write_text(code, encoding="utf-8")
        test_file.write_text(test_code, encoding="utf-8")

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "-q",
                    "--tb=short",
                    str(test_file),
                ],
                cwd=workspace,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                check=False,
            )

            return {
                "status": (
                    "passed" if result.returncode == 0
                    else "failed"
                ),
                "exit_code": result.returncode,
                "command": "python -m pytest -q --tb=short test_candidate.py",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "baseline_code": code,
                "evidence_captured": True,
            }

        except subprocess.TimeoutExpired as exc:
            return {
                "status": "timeout",
                "exit_code": None,
                "command": "python -m pytest -q --tb=short test_candidate.py",
                "stdout": exc.stdout or "",
                "stderr": exc.stderr or "",
                "baseline_code": code,
                "evidence_captured": True,
            }
