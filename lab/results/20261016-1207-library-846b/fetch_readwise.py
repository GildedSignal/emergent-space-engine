#!/usr/bin/env python3
"""Fetch (or reuse cached) Readwise export and flatten to highlights.jsonl.

Usage:
  python3 fetch_readwise.py            # fetch if cache missing, else reuse
  python3 fetch_readwise.py --refetch  # force re-fetch

Writes:
  cache/readwise-export.json   (raw pages, merged)
  cache/highlights.jsonl       (one line per highlight: title, author, text)
"""
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
RAW = os.path.join(CACHE, "readwise-export.json")
OUT = os.path.join(CACHE, "highlights.jsonl")
TOKEN = os.environ.get("READWISE_TOKEN", "")


def fetch_all():
    pages = []
    cursor = ""
    n = 0
    while True:
        url = "https://readwise.io/api/v2/export/"
        if cursor:
            url += "?pageCursor=" + urllib.parse.quote(str(cursor))
        req = urllib.request.Request(url, headers={"Authorization": "Token " + TOKEN})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read().decode("utf-8"))
        pages.append(data)
        n += 1
        cursor = data.get("nextPageCursor")
        print(f"page {n}: {len(data.get('results', []))} books", file=sys.stderr)
        if not cursor:
            break
    return pages


def main():
    os.makedirs(CACHE, exist_ok=True)
    if TOKEN and (not os.path.exists(RAW) or "--refetch" in sys.argv):
        pages = fetch_all()
        with open(RAW, "w") as f:
            json.dump({"pages": pages}, f)
        print(f"fetched {len(pages)} pages -> {RAW}", file=sys.stderr)
    elif not os.path.exists(RAW):
        sys.exit("no cache and no READWISE_TOKEN")

    with open(RAW) as f:
        pages = json.load(f)["pages"]

    n = 0
    seen = set()
    with open(OUT, "w") as f:
        for page in pages:
            for book in page.get("results", []):
                title = book.get("title", "") or ""
                author = ", ".join(book.get("author", "") or []) if isinstance(book.get("author"), list) else (book.get("author") or "")
                cat = book.get("category", "")
                src = book.get("source", "")
                for h in book.get("highlights", []):
                    text = (h.get("text") or "").strip()
                    if not text:
                        continue
                    hid = h.get("id")
                    if hid is not None and hid in seen:
                        continue
                    if hid is not None:
                        seen.add(hid)
                    note = (h.get("note") or "").strip()
                    f.write(json.dumps({
                        "title": title, "author": author, "category": cat,
                        "source": src, "text": text, "note": note,
                    }, ensure_ascii=False) + "\n")
                    n += 1
    print(f"{n} highlights -> {OUT}")


if __name__ == "__main__":
    main()
