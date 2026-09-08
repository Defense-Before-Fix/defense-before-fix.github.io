# defense-before-fix.github.io

The US spelling. A signpost: one page per primary path of the canonical site, each with a plain
link to its counterpart at <https://defence-before-fix.github.io/>. No automatic redirects.

Everything on these pages comes from the canonical repository's `_data/site.yml`, published as
`/site.json`, and the stylesheet is linked from the canonical site. Edit there, never here.
`python3 generate.py` rebuilds the pages from the live JSON (`--local` reads the sibling checkout's
YAML instead); the `regenerate` workflow does the same daily and on demand.
