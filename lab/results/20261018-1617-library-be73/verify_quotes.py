#!/usr/bin/env python3
"""verify_quotes.py — every carried quote must appear byte-identical in the export.

Reads work/readwise.json (the cached full export, 4,590 highlights). Exits 1 if
any fragment is not found verbatim in the cited source."""

import json, sys

CACHE = "work/readwise.json"
# fragment -> (cited source title, cited author)
FRAGMENTS = {
    "Limited work in progress improves efficiency by preventing overwhelming overhead.":
        ("#722 —  Cal Newport — How to Embrace Slow Productivity, Build a Deep Life, Achieve Mastery, and Defend Your Time", "The Tim Ferriss Show"),
    "Be quick to say no and slow to say yes. Saying yes consumes time. Saying no creates time.":
        ("The Focus to Say No", "Farnam Street"),
    "Rules that made sense when they were written may well be obsolete. Make them extinct, too":
        ("Lessons on Leadership: Michael Abrashoff on Turning the Worst Ship in the Navy Into the Best", "Farnam Street"),
    "every single piece has a principle of motion of its own":
        ("The Chessboard Fallacy", "Farnam Street"),
    "Anyone looks like a genius when they":
        ("Leverage Time", "Farnam Street"),
}

data = json.load(open(CACHE))
n = sum(len(b.get("highlights") or []) for b in data)
print(f"indexed {n} highlights from {len(data)} books")
fails = 0
for frag, (title, author) in FRAGMENTS.items():
    srcs = [(b["title"], b.get("author") or "?") for b in data
            for h in (b.get("highlights") or []) if frag in h["text"]]
    ok = any(t == title and a == author for t, a in srcs)
    tag = "OK  " if ok else "FAIL"
    if not ok:
        fails += 1
    print(f"{tag} [{author}] {frag[:58]}... -> found in {srcs}")
sys.exit(1 if fails else 0)
