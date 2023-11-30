import re
from pathlib import Path


with open(Path("docs/source/changelog.md")) as fh:
    raw = fh.read()

out = []
raw_split = raw.splitlines()
line_number = 0
while line_number < len(raw_split):
    line = raw_split[line_number]
    if line.startswith("- "):
        note = [line.strip()]
        line_number += 1
        line = raw_split[line_number]
        while line and not line.startswith("-"):
            note.append(line.strip())
            try:
                line_number += 1
                line = raw_split[line_number]
            except IndexError:
                line = ""
                line_number = len(raw_split) + 2

        note = " ".join(note)
        parts = re.match(r"-   (?P<mr>\(\S*\)) (?P<desc>.*)", note)
        new_note = f"- {parts.group('desc')} {parts.group('mr')}"
        out.append(new_note)

        if line.startswith("-"):
            line_number -= 1
        else:
            out.append(line)

    else:
        out.append(line)

    line_number += 1

print("\n".join(out))
