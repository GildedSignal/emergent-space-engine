#!/usr/bin/env python3
"""Rebuild work/readwise.json from the cached raw export (work/readwise_raw.json).
Refetches the raw export only if the cache is missing AND READWISE_TOKEN is set."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'readwise_raw.json')
OUT = os.path.join(HERE, 'readwise.json')

def fetch():
    import urllib.request
    token = os.environ['READWISE_TOKEN']
    pages, cursor = [], None
    while True:
        url = "https://readwise.io/api/v2/export/" + (f"?pageCursor={cursor}" if cursor else "")
        req = urllib.request.Request(url, headers={"Authorization": "Token " + token})
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.load(r)
        pages.append(d)
        cursor = d.get('nextPageCursor')
        if not cursor:
            break
    json.dump(pages, open(RAW, 'w'))

if not os.path.exists(RAW):
    if 'READWISE_TOKEN' not in os.environ:
        sys.exit("readwise_raw.json missing and READWISE_TOKEN unset")
    fetch()

pages = json.load(open(RAW))
books = []
for p in pages:
    for b in p.get('results', []):
        if b.get('is_deleted'):
            continue
        hl = [h['text'] for h in (b.get('highlights') or []) if h.get('text')]
        if not hl:
            continue
        books.append({'title': b.get('title') or '', 'author': b.get('author') or '',
                      'category': b.get('category') or '', 'n': len(hl), 'highlights': hl})
json.dump(books, open(OUT, 'w'))
print(f"cache: {len(books)} books, {sum(b['n'] for b in books)} highlights")
