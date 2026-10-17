#!/usr/bin/env python3
"""Consolidate the Readwise export pages into highlights.jsonl."""
import json, glob

rows = []
for f in sorted(glob.glob('page_*.json')):
    d = json.load(open(f))
    for b in d.get('results', []):
        title = b.get('title') or ''
        au = b.get('author')
        if isinstance(au, list):
            author = ', '.join((a.get('name', '') if isinstance(a, dict) else str(a)) for a in au)
        elif isinstance(au, dict):
            author = au.get('name', '')
        else:
            author = au or ''
        for h in (b.get('highlights') or []):
            t = (h.get('text') or '').strip()
            if t:
                rows.append({'t': t, 'b': title, 'a': author})
with open('highlights.jsonl', 'w') as fh:
    for r in rows:
        fh.write(json.dumps(r, ensure_ascii=False) + '\n')
print(f'indexed {len(rows)} highlights')
