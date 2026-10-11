#!/usr/bin/env python3
"""Search Julien's Readwise highlights. Usage: hl.py 'regex1' 'regex2' ..."""
import json, re, sys

d = json.load(open(__file__.rstrip('hl.py') + 'readwise.json'))
docs = [r for p in d for r in p['results'] if not r.get('is_deleted')]
rows = []
for r in docs:
    for h in r.get('highlights', []):
        rows.append((r.get('title', '?'), r.get('author', '?'), h.get('text', ''), h.get('location', '')))


def search(pat, limit=10, width=360):
    rx = re.compile(pat, re.I)
    hits = [(t, a, tx.strip().replace('\n', ' ')) for t, a, tx, l in rows if rx.search(tx)]
    print(f"### /{pat}/ -> {len(hits)} hits")
    for t, a, tx in hits[:limit]:
        print(f"[{a} | {t[:48]}] {tx[:width]}")
    print()


if __name__ == '__main__':
    for pat in sys.argv[1:]:
        search(pat)
