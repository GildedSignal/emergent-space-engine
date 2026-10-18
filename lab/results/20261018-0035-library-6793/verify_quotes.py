#!/usr/bin/env python3
"""verify_quotes.py — the five dossier quotes, byte-verified against a Readwise export.

Usage: verify_quotes.py [highlights.json]  (default: work/highlights.json, fetched fresh
by regen.sh; the author's cached copy is work/highlights.json from this run's own fetch).
Prints one line per quote: BYTE-IDENTICAL / DIFFERS / NOT FOUND, and exits nonzero on any
non-identical quote.
"""
import json, sys, os, urllib.request, urllib.parse

QUOTES = [
    # (verbatim quote fragment, author, title)
    ("The one thing you have to avoid is the risk of ruin.",
     "Eric Jorgenson, Jack Butcher, and Tim Ferriss", "The Almanack of Naval Ravikant"),
    ("It is better to be roughly right than precisely wrong.",
     "Josh Kaufman", "The Personal MBA 10th Anniversary Edition"),
    ("A lot of extraordinary things in life are the result of things that are first-order negative, second order positive.",
     "Farnam Street", "Second-Order Thinking: What Smart People Use to Outperform"),
    ("A helpful rule of thumb is that each layer of highlighting should include no more than 10\u201320 percent of the previous layer.",
     "Tiago Forte", "Building a Second Brain"),
    ("Make reversible decisions as soon as possible and make irreversible decisions as late as possible.",
     "Farnam Street", "Reversible and Irreversible Decisions"),
]

path = sys.argv[1] if len(sys.argv) > 1 else "work/highlights.json"
if not os.path.exists(path):
    tok = os.environ["READWISE_TOKEN"]; cur = None; out = []
    while True:
        url = "https://readwise.io/api/v2/export/"
        if cur: url += "?pageCursor=" + urllib.parse.quote(str(cur))
        req = urllib.request.Request(url, headers={"Authorization": f"Token {tok}"})
        d = json.load(urllib.request.urlopen(req)); out.extend(d.get("results", []))
        cur = d.get("nextPageCursor")
        if not cur: break
    flat = []
    for b in out:
        for h in b.get("highlights", []):
            h["title"], h["author"] = b.get("title"), b.get("author"); flat.append(h)
    os.makedirs("work", exist_ok=True)
    json.dump(flat, open(path, "w")); path_ok = True
else:
    path_ok = True

H = json.load(open(path))
bad = 0
for frag, author, title in QUOTES:
    hit = next((h for h in H if frag in h.get("text", "")
                and (h.get("author") or "") == author
                and (h.get("title") or "") == title), None)
    if hit is None:
        near = next((h for h in H if frag[:40] in h.get("text", "")), None)
        status = "DIFFERS (author/title mismatch)" if near else "NOT FOUND"; bad += 1
    else:
        status = "BYTE-IDENTICAL"
    print(f"[{status}] {author} — {title}")
    print(f"    \"{frag[:80]}...\"" if len(frag) > 80 else f"    \"{frag}\"")
print(f"highlights in export: {len(H)}; quotes verified: {len(QUOTES)}; failures: {bad}")
sys.exit(1 if bad else 0)
