#!/usr/bin/env python3
"""Measure the Runs-list disease on a wiki directory: lines, distinct ids, duplicated lines per page."""
import json, os, re, sys

def runs_of(text):
    m = re.search(r"^## Runs\s*$", text, re.M)
    if not m:
        return []
    rest = text[m.end():]
    end = re.search(r"^## ", rest, re.M)
    return [l for l in (rest[:end.start()] if end else rest).splitlines() if l.startswith("- ")]

wiki = sys.argv[1]
pages = {}
for name in sorted(os.listdir(wiki)):
    if not name.endswith(".md") or name in ("index.md", "README.md"):
        continue
    lines = runs_of(open(os.path.join(wiki, name), encoding="utf-8").read())
    ids = [re.match(r"^- (\S+)", l).group(1) for l in lines if re.match(r"^- (\S+)", l)]
    pages[name] = {"lines": len(lines), "ids": len(set(ids)), "dups": len(ids) - len(set(ids))}
print(json.dumps({"n_pages": len(pages),
                  "n_diseased": sum(1 for v in pages.values() if v["dups"] > 0),
                  "dup_lines_total": sum(v["dups"] for v in pages.values()),
                  "pages": pages}))
