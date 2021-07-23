"""Extract the changelog for the current version."""

import subprocess

from dephell_changelogs import parse_changelog

with open("./CHANGELOG.rst") as fd:
    cl = parse_changelog(fd.read())
tag = subprocess.run(
    ["git", "describe", "--tags"], stdout=subprocess.PIPE
).stdout.decode()
if tag[0] != "v":
    raise ValueError(f"git tag is not a version: {tag!r}")
version = tag[1:-1]

print(cl[version])
