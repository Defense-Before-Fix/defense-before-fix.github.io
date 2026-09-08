#!/usr/bin/env python3
"""Generate the mirror of the canonical site's primary pages.

Every page here is a disambiguation redirect: the US spelling resolves to the
British-spelled canonical page. Run after adding a page to the list, commit the
output.
"""

from pathlib import Path

CANONICAL = "https://defence-before-fix.github.io"

# (path on this site, path on the canonical site, human title)
# (path on this site, path on the canonical site, human title, what the reader will find there)
PAGES = [
    ("index.html", "/", "Defence Before Fix",
     "The home page: the definition, the six clauses, the documents, the tools that implement the method and the article in which it was first published."),
    ("SPEC.html", "/SPEC.html", "the method specification",
     "Method specification 1.0.0, the normative document: what a practitioner does when a defect is found, in six numbered clauses with the reasoning for each, conformance for a remediation, a rule and a toolchain, and how the method operates under AI-assisted development."),
    ("TOOLING-SPEC.html", "/TOOLING-SPEC.html", "the toolchain specification",
     "Toolchain specification 0.1.0, addressed to anyone who maintains a linter, static analyser or QA pipeline: what a tool must offer so that the projects using it can follow the method, and what it takes to claim conformance."),
    ("PRIMER.html", "/PRIMER.html", "the primer",
     "The short introduction, written at reading pace: why the bug you have just found is evidence worth keeping, and why the net is built before the catch is landed."),
    ("PROVENANCE.html", "/PROVENANCE.html", "provenance",
     "Who coined the term, when it was first published, and what is and is not being claimed for it."),
    ("CHANGELOG.html", "/CHANGELOG.html", "the changelog",
     "Changes to each document, versioned independently, so that a toolchain clause can be added without reissuing the method."),
    ("tools/index.html", "/tools/", "the tools register",
     "A register of QA tools grouped by language, each graded for readiness and for conformance, with a page per tool saying how it is and is not conformant, clause by clause."),
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
    <nav aria-label="Canonical site">
      <a href="https://defence-before-fix.github.io/SPEC.html">Method specification</a>
      <a href="https://defence-before-fix.github.io/TOOLING-SPEC.html">Toolchain specification</a>
      <a href="https://defence-before-fix.github.io/PRIMER.html">Primer</a>
      <a href="https://defence-before-fix.github.io/tools/">Tools</a>
      <a href="https://defence-before-fix.github.io/PROVENANCE.html">Provenance</a>
      <a href="https://defence-before-fix.github.io/CHANGELOG.html">Changelog</a>
    </nav>
    <p class="site-byline">The US spelling of Defence Before Fix, a method by
      <a href="https://ltscommerce.dev">Joseph Edmonds</a> of
      <a href="https://edmondscommerce.co.uk">Edmonds Commerce</a>. First published 22 February 2026.</p>
  </header>
  <main>
    <div class="disambiguation">
      <h1>{heading}</h1>
      <p>Defence Before Fix is a phase that runs before a defect is fixed: the instance is treated
        as evidence of a class, and the defence that detects the class is built and seen to fire
        before the fix is made. It is published under the British spelling; this site exists so
        that the US spelling finds the right place.</p>
      <p>{blurb}</p>
      <p><a class="go" href="{target}">Read {title} on defence-before-fix.github.io</a></p>
      <p class="site-byline">This site is a signpost. Nothing is published here; every document
        lives, with its history, on the canonical site.</p>
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
    for local, remote, title, blurb in PAGES:
        target = CANONICAL + remote
        out = root / local
        out.parent.mkdir(parents=True, exist_ok=True)
        depth = len(Path(local).parts) - 1
        prefix = "../" * depth
        heading = "Defense Before Fix" if remote == "/" else title[0].upper() + title[1:]
        out.write_text(
            TEMPLATE.format(
                title=title,
                blurb=blurb,
                target=target,
                heading=heading,
                css=f"{prefix}assets/css/site.css",
                home=f"{prefix}index.html" if prefix else "./",
            )
        )
        print(f"wrote {local} -> {target}")


if __name__ == "__main__":
    main()
