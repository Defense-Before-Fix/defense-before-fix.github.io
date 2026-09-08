#!/usr/bin/env python3
"""Generate the mirror of the canonical site's primary pages.

Every page here is a disambiguation redirect: the US spelling resolves to the
British-spelled canonical page. Run after adding a page to the list, commit the
output.
"""

from pathlib import Path

CANONICAL = "https://defence-before-fix.github.io"

# (path on this site, path on the canonical site, human title)
PAGES = [
    ("index.html", "/", "Defence Before Fix"),
    ("SPEC.html", "/SPEC.html", "the method specification"),
    ("TOOLING-SPEC.html", "/TOOLING-SPEC.html", "the toolchain specification"),
    ("PRIMER.html", "/PRIMER.html", "the primer"),
    ("PROVENANCE.html", "/PROVENANCE.html", "provenance"),
    ("CHANGELOG.html", "/CHANGELOG.html", "the changelog"),
    ("tools/index.html", "/tools/", "the tools register"),
]

TEMPLATE = """<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <title>Defense Before Fix (US spelling): {title}</title>
  <link rel="canonical" href="{target}">
</head>
<body>
  <h1>Defense Before Fix</h1>
  <p>Defense Before Fix is the US spelling of Defence Before Fix, a phase that runs before a
    defect is fixed. This page exists so that the US spelling finds the right place; nothing is
    published under it.</p>
  <p>Read <a href="{target}">{title}</a> on the canonical site, defence-before-fix.github.io.</p>
</body>
</html>
"""


def main() -> None:
    root = Path(__file__).parent
    for local, remote, title in PAGES:
        target = CANONICAL + remote
        out = root / local
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(TEMPLATE.format(title=title, target=target))
        print(f"wrote {local} -> {target}")


if __name__ == "__main__":
    main()
