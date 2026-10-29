from app.services.patch_engine import apply_unified_diff


def test_valid_patch_changes_source():
    original = "def add(a, b):\n    return a - b\n"
    patch = (
        "--- a/candidate.py\n"
        "+++ b/candidate.py\n"
        "@@ -1,2 +1,2 @@\n"
        " def add(a, b):\n"
        "-    return a - b\n"
        "+    return a + b\n"
    )

    result = apply_unified_diff(original, patch)

    assert result.valid is True
    assert result.patched_code == "def add(a, b):\n    return a + b\n"


def test_rejects_wrong_target_path():
    result = apply_unified_diff(
        "x = 1\n",
        "--- a/other.py\n+++ b/other.py\n@@ -1 +1 @@\n-x = 1\n+y = 2\n",
    )

    assert result.valid is False
    assert result.patched_code is None


def test_rejects_context_that_does_not_match():
    result = apply_unified_diff(
        "x = 1\n",
        "--- a/candidate.py\n+++ b/candidate.py\n@@ -1 +1 @@\n-x = 99\n+y = 2\n",
    )

    assert result.valid is False
    assert "context does not match" in result.error


def test_rejects_empty_patch():
    result = apply_unified_diff("x = 1\n", "")

    assert result.valid is False


def test_original_code_is_not_modified():
    original = "x = 1\n"
    patch = (
        "--- a/candidate.py\n"
        "+++ b/candidate.py\n"
        "@@ -1 +1 @@\n"
        "-x = 1\n"
        "+x = 2\n"
    )

    apply_unified_diff(original, patch)

    assert original == "x = 1\n"

def test_rejects_path_traversal_target():
    result = apply_unified_diff(
        "x = 1\n",
        "--- a/../candidate.py\n+++ b/../candidate.py\n@@ -1 +1 @@\n-x = 1\n+y = 2\n",
        target_filename="../candidate.py",
    )
    assert result.valid is False
    assert result.patched_code is None


def test_rejects_multi_file_patch():
    patch = (
        "--- a/candidate.py\n"
        "+++ b/candidate.py\n"
        "@@ -1 +1 @@\n"
        "-x = 1\n"
        "+x = 2\n"
        "--- a/other.py\n"
        "+++ b/other.py\n"
        "@@ -1 +1 @@\n"
        "-y = 1\n"
        "+y = 2\n"
    )
    result = apply_unified_diff("x = 1\n", patch)
    assert result.valid is False


def test_rejects_malformed_hunk_header():
    patch = (
        "--- a/candidate.py\n"
        "+++ b/candidate.py\n"
        "@@ invalid @@\n"
        "-x = 1\n"
        "+x = 2\n"
    )
    result = apply_unified_diff("x = 1\n", patch)
    assert result.valid is False


def test_rejects_incorrect_hunk_line_counts():
    patch = (
        "--- a/candidate.py\n"
        "+++ b/candidate.py\n"
        "@@ -1,2 +1,2 @@\n"
        "-x = 1\n"
        "+x = 2\n"
    )
    result = apply_unified_diff("x = 1\n", patch)
    assert result.valid is False
