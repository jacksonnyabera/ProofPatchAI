from dataclasses import dataclass
import re


@dataclass(frozen=True)
class PatchResult:
    valid: bool
    patched_code: str | None
    error: str | None = None


def apply_unified_diff(
    original_code: str,
    patch: str,
    target_filename: str = "candidate.py",
) -> PatchResult:
    """Validate and apply a single-file unified diff in memory only."""
    if not original_code:
        return PatchResult(False, None, "Original code cannot be empty")

    if not patch.strip():
        return PatchResult(False, None, "Patch cannot be empty")

    if (
        not target_filename
        or "/" in target_filename
        or "\\" in target_filename
        or target_filename in {".", ".."}
        or not re.fullmatch(r"[A-Za-z0-9_.-]+", target_filename)
    ):
        return PatchResult(False, None, "Invalid target filename")

    lines = patch.splitlines()
    if len(lines) < 4:
        return PatchResult(False, None, "Patch is incomplete")

    if lines[0] != f"--- a/{target_filename}":
        return PatchResult(False, None, "Unexpected original file path")

    if lines[1] != f"+++ b/{target_filename}":
        return PatchResult(False, None, "Unexpected patched file path")

    source = original_code.splitlines()
    output = []
    source_index = 0
    patch_index = 2

    while patch_index < len(lines):
        match = re.fullmatch(
            r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(?:.*)",
            lines[patch_index],
        )
        if not match:
            return PatchResult(False, None, "Invalid hunk header")

        old_start = int(match.group(1))
        old_count = int(match.group(2) or 1)
        new_count = int(match.group(4) or 1)
        expected_index = old_start - 1 if old_count else old_start

        if expected_index < source_index or expected_index > len(source):
            return PatchResult(False, None, "Hunk is outside the source file")

        output.extend(source[source_index:expected_index])
        source_index = expected_index
        patch_index += 1
        removed = 0
        added = 0

        while patch_index < len(lines) and not lines[patch_index].startswith("@@ "):
            line = lines[patch_index]

            if line.startswith("--- ") or line.startswith("+++ "):
                return PatchResult(False, None, "Multi-file patches are not allowed")

            if line == r"\ No newline at end of file":
                patch_index += 1
                continue

            if not line or line[0] not in " +-":
                return PatchResult(False, None, "Invalid diff line")

            content = line[1:]

            if line[0] in " -":
                if source_index >= len(source):
                    return PatchResult(False, None, "Patch removes missing source lines")
                if source[source_index] != content:
                    return PatchResult(False, None, "Patch context does not match source")
                if line[0] == " ":
                    output.append(source[source_index])
                source_index += 1
                removed += 1

            if line[0] == "+":
                output.append(content)
            if line[0] in " +":
                added += 1

            patch_index += 1

        if removed != old_count or added != new_count:
            return PatchResult(False, None, "Hunk line counts do not match header")

    output.extend(source[source_index:])
    patched = "\n".join(output)

    if original_code.endswith("\n"):
        patched += "\n"

    if patched == original_code:
        return PatchResult(False, None, "Patch does not change the source")

    return PatchResult(True, patched)
