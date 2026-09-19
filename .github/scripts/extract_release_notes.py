"""Extract one version's notes from docs/src/release_notes.rst as Markdown.

Prints the notes for the requested version to stdout, or nothing at all when the
changelog has no entry for it. GitHub renders release bodies as Markdown, so the
reStructuredText section underlines are converted to Markdown headings on the way
out. Anything printed here is prepended to GitHub's generated "What's Changed"
list by the github-release workflow.
"""

import re
import sys
from pathlib import Path

RELEASE_NOTES = (
    Path(__file__).resolve().parents[2] / "docs" / "src" / "release_notes.rst"
)

# A version heading looks like "3.7.1 (2025-08-17)" or just "3.7.3", underlined with dashes.
VERSION_HEADING = re.compile(r"^(?P<version>\d+\.\d+\.\d+)\s*(?:\(.*\))?\s*$")
UNDERLINE = re.compile(r"^(?P<char>[-=*~^\"'#+`])(?P=char)+\s*$")


def section_for(lines: list[str], version: str) -> list[str]:
    """Return the lines belonging to `version`, excluding its own heading."""
    start = None
    for index, line in enumerate(lines[:-1]):
        match = VERSION_HEADING.match(line)
        if not match or not UNDERLINE.match(lines[index + 1]):
            continue
        if start is None:
            if match.group("version") == version:
                start = index + 2  # Skip the heading and its underline
        else:
            return lines[start:index]  # The next version heading ends the section
    return lines[start:] if start is not None else []


def to_markdown(lines: list[str]) -> str:
    """Convert the subsection underlines in an RST section to Markdown headings."""
    converted: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        next_line = lines[index + 1] if index + 1 < len(lines) else ""
        if line.strip() and UNDERLINE.match(next_line):
            converted.append(f"### {line.strip()}")
            index += 2
            continue
        converted.append(line)
        index += 1
    return "\n".join(converted).strip()


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} VERSION", file=sys.stderr)
        return 2

    version = sys.argv[1]
    if not RELEASE_NOTES.is_file():
        print(f"No changelog at {RELEASE_NOTES}", file=sys.stderr)
        return 0

    lines = RELEASE_NOTES.read_text(encoding="utf-8").splitlines()
    section = section_for(lines, version)
    if not section:
        print(f"No changelog entry for {version}", file=sys.stderr)
        return 0

    print(to_markdown(section))
    return 0


if __name__ == "__main__":
    sys.exit(main())
