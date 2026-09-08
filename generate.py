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
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <title>Defense Before Fix (US spelling): {title}</title>
  <link rel="canonical" href="{target}">
  <link rel="stylesheet" href="{css}">
</head>
<body>
  <header class="site-header">
    <p class="site-title"><a href="{home}">Defense Before Fix</a></p>
    <p class="site-byline">The US spelling of Defence Before Fix, a method by
      <a href="https://ltscommerce.dev">Joseph Edmonds</a> of
      <a href="https://edmondscommerce.co.uk">Edmonds Commerce</a>.</p>
  </header>
  <main>
    <div class="disambiguation">
      <h1>{heading}</h1>
      <p>Defence Before Fix is a phase that runs before a defect is fixed: the instance is treated
        as evidence of a class, and the defence that detects the class is built and seen to fire
        before the fix is made. It is published under the British spelling; this site exists so
        that the US spelling finds the right place.</p>
      <p><a class="go" href="{target}">Read {title} on defence-before-fix.github.io</a></p>
    </div>
  </main>
  <footer class="site-footer">
    <p>Canonical site: <a href="https://defence-before-fix.github.io/">defence-before-fix.github.io</a>.
      Licensed under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.</p>
  </footer>
</body>
</html>
"""


def main() -> None:
    root = Path(__file__).parent
    for local, remote, title in PAGES:
        target = CANONICAL + remote
        out = root / local
        out.parent.mkdir(parents=True, exist_ok=True)
        depth = len(Path(local).parts) - 1
        prefix = "../" * depth
        heading = "Defense Before Fix" if remote == "/" else title[0].upper() + title[1:]
        out.write_text(
            TEMPLATE.format(
                title=title,
                target=target,
                heading=heading,
                css=f"{prefix}assets/css/site.css",
                home=f"{prefix}index.html" if prefix else "./",
            )
        )
        print(f"wrote {local} -> {target}")


if __name__ == "__main__":
    main()
