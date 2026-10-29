
from app.services.bug_reproducer import reproduce_python_bug


def test_reproducer_captures_a_real_failure():
    code = """
def add(a, b):
    return a - b
"""

    test_code = """
def test_add():
    assert add(2, 3) == 5
"""

    report = reproduce_python_bug(code, test_code)

    assert report["status"] == "failed"
    assert report["exit_code"] != 0
    assert report["evidence_captured"] is True
    assert "assert -1 == 5" in report["stdout"]


def test_reproducer_captures_a_passing_baseline():
    code = """
def add(a, b):
    return a + b
"""

    test_code = """
def test_add():
    assert add(2, 3) == 5
"""

    report = reproduce_python_bug(code, test_code)

    assert report["status"] == "passed"
    assert report["exit_code"] == 0
