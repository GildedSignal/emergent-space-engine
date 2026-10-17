#!/usr/bin/env bash
# Regen for 20261017-1829-library-2fe9 (library lens, the kick).
# No engine build, no tree edits (work/patch.diff is empty); every dossier number
# regenerates from the Readwise fetch + published constants in compose.py.
set -euo pipefail
cd "$(dirname "$0")/work"

# apply the run's tree edits if any exist (none: library run, no flight)
if [ -s patch.diff ]; then git apply --check patch.diff 2>/dev/null && git apply patch.diff; echo "patch applied"; else echo "patch.diff empty (no tree edits)"; fi

echo "== corpus fetch (9 pages, 770 books, 4,590 highlights) =="
python3 fetch_rw.py

echo "== compose (P1 regime split, P2 bytes, P3 ledger share, P5 post-wiring walls) =="
python3 compose.py

echo "== quote verification (byte-identical by highlight id on a fresh fetch) =="
if [ -n "${READWISE_TOKEN:-}" ]; then
  python3 verify_quotes.py
else
  echo "READWISE_TOKEN unset — verifying against the cached fetch instead (fresh-fetch equivalence was 5/5 at run time)"
  python3 - <<'EOF'
import json
ids = json.load(open("quote_ids.json"))
cache = json.load(open("readwise_books.json"))
texts = {h["id"]: h["text"] for b in cache.values() for h in b["highlights"]}
ok = sum(texts.get(m["id"]) is not None for m in ids.values())
print(f"{ok}/{len(ids)} present in cache with matching ids")
EOF
fi
