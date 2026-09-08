#!/usr/bin/env python3
"""Generate the US-spelling signpost site from the canonical site's metadata.

The single source of the shared metadata is `_data/site.yml` in the canonical
repository (Defence-Before-Fix/defence-before-fix.github.io), which the canonical
site publishes as /site.json. This script fetches that JSON, or reads the YAML
from a sibling checkout when `--local` is given, and writes one signpost page per
primary path. The stylesheet is linked from the canonical site, so it too has one
home. Nothing here is edited by hand except this script.
"""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

CANONICAL = "https://defence-before-fix.github.io"
LOCAL_DATA = Path(__file__).parent.parent / "defence-before-fix" / "_data" / "site.yml"

TEMPLATE = """<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <title>International spelling redirect page for: {heading}</title>
  <link rel="canonical" href="{target}">
  <link rel="stylesheet" href="{stylesheet}">
</head>
<body>
  <header class="site-header">
    <p class="site-title"><a href="{canonical}/">{name} ({short})</a></p>
    <nav aria-label="Canonical site">
{nav}
    </nav>
    <p class="site-byline">{name} ({short}) is a method by
      <a href="{author_url}">{author}</a> of
      <a href="{org_url}">{org}</a>, first published {coined}.</p>
  </header>
  <main>
    <div class="disambiguation">
      <p class="site-byline">International spelling redirect page for:</p>
      <h1>{heading}</h1>
      <p>{definition} It is published under the British spelling; this site exists so that the
        US spelling finds the right place.</p>
      <p>{blurb}</p>
      <p><a class="go" href="{target}">Read {title} on {canonical_host}</a></p>
      <p class="site-byline">This site is a signpost. Nothing is published here; every document
        lives, with its history, on the canonical site.</p>
    </div>
  </main>
  <footer class="site-footer">
    <p>Method specification {method} and toolchain specification {toolchain}, both published
      {published}. Canonical site: <a href="{canonical}/">{canonical_host}</a>.
      Licensed under <a href="{licence_url}">{licence}</a>.</p>
  </footer>
</body>
</html>
"""


def load() -> dict:
    if "--local" in sys.argv:
        import yaml  # PyYAML, only needed for the offline path

        return yaml.safe_load(LOCAL_DATA.read_text())
    with urllib.request.urlopen(f"{CANONICAL}/site.json", timeout=30) as response:
        return json.load(response)


def local_path(remote: str) -> Path:
    if remote == "/":
        return Path("index.html")
    if remote.endswith("/"):
        return Path(remote.strip("/")) / "index.html"
    return Path(remote.lstrip("/"))


RAW_SIGNPOST = """# International spelling redirect: {heading}

Defense Before Fix is the US spelling of Defence Before Fix. Nothing is published under this
spelling. The document you want is at:

{target}

{blurb}

Index of everything on the canonical site: {canonical}{agent_index}
"""


def main() -> None:
    data = load()
    root = Path(__file__).parent
    canonical = data["canonical_url"].rstrip("/")
    agent_index = data.get("agent_index", "/llms.txt")
    (root / agent_index.lstrip("/")).write_text(
        f"# {data['us_name']}\n\n> The US spelling of {data['name']}. This site is a signpost; "
        f"nothing is published here.\n\n- [Canonical llms.txt]({canonical}{agent_index})\n"
        f"- [Project prompt for agents]({canonical}/defence-before-fix-project-prompt.md)\n"
    )
    print(f"wrote {agent_index.lstrip('/')} -> {canonical}{agent_index}")
    nav = "\n".join(
        f'      <a href="{canonical}{p["path"]}">{p["nav"]}</a>'
        for p in data["pages"]
        if p["path"] != "/"
    )
    for page in data["pages"]:
        out = root / local_path(page["path"])
        out.parent.mkdir(parents=True, exist_ok=True)
        if page["path"].endswith(".md"):
            out.write_text(
                RAW_SIGNPOST.format(
                    heading=page["heading"],
                    target=f"{canonical}{page['path']}",
                    blurb=page["blurb"],
                    canonical=canonical,
                    agent_index=agent_index,
                )
            )
            print(f"wrote {out.relative_to(root)} -> {canonical}{page['path']} (raw markdown)")
            continue
        title = page["title"]
        heading = page["heading"]
        out.write_text(
            TEMPLATE.format(
                us_name=data["us_name"],
                name=data["name"],
                short=data.get("short", "DBF"),
                title=title,
                heading=heading,
                blurb=page["blurb"],
                target=f"{canonical}{page['path']}",
                stylesheet=f"{canonical}{data['stylesheet']}",
                nav=nav,
                author=data["author"]["name"],
                author_url=data["author"]["url"],
                org=data["organisation"]["name"],
                org_url=data["organisation"]["url"],
                coined=data["coined"],
                definition=data["definition"],
                canonical=canonical,
                canonical_host=canonical.removeprefix("https://"),
                method=data["versions"]["method"],
                toolchain=data["versions"]["toolchain"],
                published=data["versions"]["published"],
                licence=data["licence"]["name"],
                licence_url=data["licence"]["url"],
            )
        )
        print(f"wrote {out.relative_to(root)} -> {canonical}{page['path']}")


if __name__ == "__main__":
    main()
