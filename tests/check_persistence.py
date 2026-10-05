#!/usr/bin/env python3
"""macOS regression using synthetic CotEditor I/O; never touches open documents.

Keep run scope and heading transformations from the production sources. Replace
only app I/O and its rich-text terminology. Separate osascript processes exercise
compiled-script writeback; a negative control must retain the fixture text.
"""

from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
LOCALS = "local locLength, selectionLength, locLines, selectionLines, looseSelect, theSelection"
MARKER = "STATE_PERSISTENCE_FIXTURE_abcdef"


def command(*args):
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f"{args[0]} failed: {result.stderr.strip()}")
    return result.stdout


def adapt(source, fixture):
    replacements = {
        'tell application "CotEditor"': "",
        'tell front document': "",
        'end tell': "",
        'if exists front document then': "if true then",
        'if coloring style is not in {"Markdown"} then': 'if "Markdown" is not in {"Markdown"} then',
        'set {locLength, selectionLength} to range of selection':
            f'set {{locLength, selectionLength}} to {{0, count (read POSIX file "{fixture}" as «class utf8»)}}',
        'set {locLines, selectionLines} to line range of selection':
            'set {locLines, selectionLines} to {1, 1}',
        'set line range of selection to {locLines, selectionLines}': "-- synthetic whole-line selection",
        'if contents of selection ends with "\\n" then set range of selection to {locLength, selectionLength - 1}':
            '-- fixtures have no terminal newline',
        'set theSelection to contents of selection':
            f'set theSelection to (read POSIX file "{fixture}" as «class utf8»)',
        'set contents of selection to ': 'return ',
        'rich text ': 'text ',
    }
    for old, new in replacements.items():
        assert old in source, f"I/O adapter needs updating: {old}"
        source = source.replace(old, new)
    # The unchanged-selection path produces no application assignment.
    return source.replace("end run", "\treturn theSelection\nend run")


with tempfile.TemporaryDirectory(prefix="heading-persistence-") as directory:
    work = Path(directory)
    fixture = work / "input.txt"
    script = work / "test.scpt"
    src = work / "test.applescript"
    long_text = "## " + (MARKER + " 日本語😀\n") * 1600 + "end"
    for direction in ("up", "down"):
        original_source = (ROOT / f"md_heading_{direction}.applescript").read_text()
        assert LOCALS in original_source
        # Check actual CotEditor terminology separately from synthetic execution.
        src.write_text(original_source)
        command("osacompile", "-o", str(script), str(src))
        source = adapt(original_source, fixture)
        cases = (long_text, long_text, "## 短い見出し😀", "# H1", "plain", long_text)
        for execute_only in (False, True):
            src.write_text(source)
            command("osacompile", *(["-x"] if execute_only else []), "-o", str(script), str(src))
            before = script.read_bytes()
            for text in cases:
                fixture.write_text(text)
                if direction == "up":
                    expected = text[1:] if text.startswith("##") else text
                else:
                    expected = ("#" if text.startswith("#") else "# ") + text
                assert command("osascript", str(script)) == expected + "\n"
                assert script.read_bytes() == before, "Compiled script saved runtime state"
            print(f"PASS {direction}, execute_only={execute_only}: heading output and byte stability")

        src.write_text(source.replace(LOCALS, "-- negative control: implicit run variables", 1))
        command("osacompile", "-o", str(script), str(src))
        before = script.read_bytes()
        fixture.write_text(long_text)
        command("osascript", str(script))
        saved = script.read_bytes()
        assert saved != before, "Negative control did not save state"
        assert MARKER.encode("utf-16-be") in saved, "Negative control did not retain fixture text"
        print(f"PASS {direction} negative control: removing locals persists selected text")
