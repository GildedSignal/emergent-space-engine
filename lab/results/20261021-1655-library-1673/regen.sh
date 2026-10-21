#!/bin/sh
# Regenerates every dossier number from the tree + a fresh Readwise fetch. ~15 s.
set -e
cd "$(dirname "$0")"
python3 - <<'EOF'
import json, urllib.request, time, os, sys
tok = os.environ.get('READWISE_TOKEN')
assert tok, "READWISE_TOKEN unset"
cursor, allr = None, []
while True:
    url = "https://readwise.io/api/v2/export/?page_size=1000"
    if cursor: url += "&pageCursor=" + str(cursor)
    req = urllib.request.Request(url, headers={"Authorization": f"Token {tok}"})
    for a in range(5):
        try:
            d = json.load(urllib.request.urlopen(req, timeout=60)); break
        except Exception:
            if a == 4: raise
            time.sleep(3*(a+1))
    allr.extend(d.get('results', [])); cursor = d.get('nextPageCursor')
    if not cursor: break
json.dump(allr, open('readwise.json', 'w'))
out = []
for b in allr:
    for h in b.get('highlights', []):
        out.append(f"### {b.get('title') or ''} | {b.get('author') or ''}\n{h.get('text') or ''}")
open('quotes.txt', 'w').write('\n\n'.join(out))
n = sum(len(b.get('highlights', [])) for b in allr)
print(f"highlights: {n}")
EOF
python3 compose_family.py
