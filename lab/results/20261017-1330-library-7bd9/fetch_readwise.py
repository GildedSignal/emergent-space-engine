#!/usr/bin/env python3
"""Fetch all Readwise highlights fresh, cache to this run folder."""
import json, os, sys, urllib.request

TOKEN = os.environ["READWISE_TOKEN"]
out = sys.argv[1] if len(sys.argv) > 1 else "readwise.json"
cursor = ""
pages = 0
highlights = []
books = {}
while True:
    url = "https://readwise.io/api/v2/export/" + (f"?pageCursor={cursor}" if cursor else "")
    req = urllib.request.Request(url, headers={"Authorization": f"Token {TOKEN}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())
    pages += 1
    for b in data.get("results", []):
        books[b["user_book_id"]] = {
            "title": b.get("title"),
            "author": b.get("author"),
            "category": b.get("category"),
            "asin": b.get("asin"),
        }
        for h in b.get("highlights", []):
            highlights.append({
                "text": h.get("text"),
                "book_id": b["user_book_id"],
                "location": h.get("location"),
                "highlighted_at": h.get("highlighted_at"),
            })
    cursor = data.get("nextPageCursor")
    if not cursor:
        break
doc = {"pages": pages, "n_highlights": len(highlights), "n_books": len(books),
       "books": books, "highlights": highlights}
with open(out, "w") as f:
    json.dump(doc, f)
print(f"pages={pages} highlights={len(highlights)} books={len(books)}")
