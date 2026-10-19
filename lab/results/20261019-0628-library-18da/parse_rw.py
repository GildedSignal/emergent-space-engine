#!/usr/bin/env python3
"""Flatten the Readwise export (pages of {count,nextPageCursor,results}) into one TSV: book, author, text."""
import json, glob, sys, csv
out = 'lab/results/20261019-0628-library-18da/readwise/highlights.tsv'
rows = []
for f in sorted(glob.glob('lab/results/20261019-0628-library-18da/readwise/page_*.json')):
    d = json.load(open(f))
    for b in d.get('results', []):
        title = b.get('title') or ''
        author = ', '.join(b.get('author') or []) if isinstance(b.get('author'), list) else (b.get('author') or '')
        for h in b.get('highlights', []):
            t = (h.get('text') or '').replace('\t', ' ').replace('\n', ' ').strip()
            if t: rows.append((title, author, t))
with open(out, 'w', newline='') as fh:
    w = csv.writer(fh, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
    w.writerow('title author text'.split())
    w.writerows(rows)
print(f"{len(rows)} highlights -> {out}")
