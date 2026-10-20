#!/usr/bin/env python3
"""Fetch the Readwise export (paginated) and build highlights_flat.json; falls back to the
kept copy when the token is absent or the network is down."""
import json, os, sys, time, urllib.request
out = os.path.join(os.path.dirname(__file__), "highlights_flat.json")
if os.environ.get("READWISE_TOKEN"):
    tok, books, cur = os.environ["READWISE_TOKEN"], [], None
    try:
        for _ in range(60):
            url = "https://readwise.io/api/v2/export/" + (f"?pageCursor={cur}" if cur else "")
            req = urllib.request.Request(url, headers={"Authorization": f"Token {tok}"})
            for a in range(5):
                try:
                    with urllib.request.urlopen(req, timeout=120) as r:
                        d = json.load(r)
                    break
                except Exception:
                    if a == 4: raise
                    time.sleep(5 * (a + 1))
            books.extend(d.get("results", []))
            cur = d.get("nextPageCursor")
            if not cur: break
        rows = [{"book": b.get("title"), "author": b.get("author"), "text": h["text"], "id": h["id"]}
                for b in books for h in b["highlights"]]
        json.dump(rows, open(out, "w"))
        print(f"fetched fresh: {len(rows)} highlights, {len(books)} books/docs")
        sys.exit(0)
    except Exception as e:
        print(f"(fetch failed: {e}; using kept copy)")
print(f"kept copy: {len(json.load(open(out)))} highlights")
