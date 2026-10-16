#!/usr/bin/env bash
# Regen: reproduce every number and quote in the dossier from the shipped tree
# plus this run's scripts. Total wall time well under 15 min (fetch ~10 s when
# the API is warm; cache reuse is instant on re-runs).
set -euo pipefail
cd "$(dirname "$0")"

echo "== 1. Readwise export (fetch if cache missing) =="
python3 fetch_readwise.py

echo "== 2. Census + verbatim quote verification =="
python3 verify_quotes.py

echo "== 3. goodreads census (books on the shelf, to-read vs read) =="
python3 - <<'EOF'
import csv, re
rd = list(csv.DictReader(open('../../../lab/library/goodreads.csv')))
print(f"{len(rd)} books on the shelf")
pat = re.compile(r"skunk|liftoff|berger|forth|fortune|thorp|shannon|kelly", re.I)
for b in rd:
    s = b.get('Title','') + ' ' + b.get('Author','')
    if pat.search(s):
        print(f"  {b.get('Author','?')[:22]:22s} | {b.get('Title','?')[:44]} | rating={b.get('My Rating','?')} {b.get('Bookshelves','')[:14]}")
EOF

echo "== 4. Deletion-bar arithmetic (7f99's audit vs Musk's 10%) =="
python3 - <<'EOF'
kills, addbacks = 26, 2
print(f"7f99 audit: {kills} kills, {addbacks} add-backs = {100*addbacks/kills:.1f}% "
      f"(Musk's bar: under 10% add-back = you did not delete enough)")
EOF

echo "REGEN OK"
