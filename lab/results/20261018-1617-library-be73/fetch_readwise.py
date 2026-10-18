#!/usr/bin/env python3
"""fetch_readwise.py — full Readwise export with pagination, cached slim to work/.

Uses READWISE_TOKEN if set (fresh fetch); otherwise the existing cache stands."""
import json, os, sys, urllib.request

TOKEN = os.environ.get("READWISE_TOKEN")
CACHE = "work/readwise.json"

def fetch(url):
    req = urllib.request.Request(url, headers={"Authorization": f"Token {TOKEN}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

if not TOKEN:
    if os.path.exists(CACHE):
        print(f"no token: using cache {CACHE}")
        sys.exit(0)
    sys.exit("no token and no cache")

books, seen, cursor, page = [], set(), None, 0
while True:
    url = "https://readwise.io/api/v2/export/" + (f"?pageCursor={cursor}" if cursor else "")
    d = fetch(url)
    page += 1
    for b in d["results"]:
        if b["user_book_id"] not in seen:
            seen.add(b["user_book_id"]); books.append(b)
    cursor = d.get("nextPageCursor")
    if not cursor:
        break

slim = [{"title": b["title"], "author": b.get("author"),
         "highlights": [{"text": h["text"]} for h in (b.get("highlights") or [])]}
        for b in books]
json.dump(slim, open(CACHE, "w"))
print(f"fetched {page} pages, {len(books)} books, "
      f"{sum(len(b.get('highlights') or []) for b in books)} highlights")
