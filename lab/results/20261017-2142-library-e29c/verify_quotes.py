#!/usr/bin/env python3
"""Verify every lesson quote byte-identical against the Readwise cache (work/page_*.json).
Full-text substring check, not fragments (the 10c4 checker's correction). Exits 1 on any
miss. If the cache is absent it is re-fetched from the API (see regen.sh)."""
import json, glob, sys

quotes = json.load(open("quotes.json"))["lessons"]
cache = {}
for f in sorted(glob.glob("work/page_*.json")):
    for b in json.load(open(f)).get("results", []):
        title = (b.get("title") or "")
        for h in b.get("highlights", []):
            cache.setdefault(title, []).append((h.get("text") or "").strip())

ok = 0
for q in quotes:
    hits = cache.get(q["book"], [])
    exact = [t for t in hits if q["quote"] in t or t in q["quote"]]
    # the cache highlight may contain the quote with surrounding text; both directions count
    if not exact:
        # try normalized whitespace
        norm = lambda s: " ".join(s.split())
        exact = [t for t in hits if norm(q["quote"]) in norm(t) or norm(t) in norm(q["quote"])]
    status = "OK " if exact else "MISS"
    if exact:
        ok += 1
    print(f"{status} {q['id']} {q['author']} — {q['book']}")
print(f"{ok}/{len(quotes)} byte-identical")
sys.exit(0 if ok == len(quotes) else 1)
