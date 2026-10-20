#!/usr/bin/env bash
# Regenenerates every dossier number: fresh Readwise fetch (token-gated, cache
# fallback), quote byte-identity, the 1e9 composition, and the code anchors.
set -euo pipefail
cd "$(dirname "$0")"
ROOT=../../..

echo "== 1. Readwise export =="
if [ -n "${READWISE_TOKEN:-}" ]; then
  mkdir -p cache && rm -f cache/page-*.json
  cursor=""; page=0
  while :; do
    page=$((page+1))
    if [ -z "$cursor" ]; then
      curl -s -H "Authorization: Token $READWISE_TOKEN" "https://readwise.io/api/v2/export/" -o "cache/page-$page.json"
    else
      curl -s -H "Authorization: Token $READWISE_TOKEN" "https://readwise.io/api/v2/export/?pageCursor=$cursor" -o "cache/page-$page.json"
    fi
    next=$(jq -r '.nextPageCursor // "null"' "cache/page-$page.json")
    [ "$next" = "null" ] && break
    cursor=$next; [ $page -gt 40 ] && break
  done
  echo "fetched fresh: $(ls cache/page-*.json | wc -l) pages"
else
  echo "READWISE_TOKEN unset: using cached export ($(ls cache/page-*.json | wc -l) pages, fetched 2026-10-20)"
fi

echo; echo "== 2. Quote byte-identity (P1) =="
python3 verify_quotes.py

echo; echo "== 3. 1e9 composition (P2) =="
python3 compose.py

echo; echo "== 4. Code anchors (P3) =="
echo "-- step.rs:717-718 (the comb inserts):"
sed -n '717,718p' "$ROOT/crates/universe/src/step.rs"
echo "-- step.rs:663-676 excerpt (kick_clock crash checks every kick, no leave check):"
sed -n '663,676p' "$ROOT/crates/universe/src/step.rs" | sed -n '1,3p;12,14p'
echo "-- step.rs:725-739 boundary_clock (surface + leave + anchor stamp):"
sed -n '725,739p' "$ROOT/crates/universe/src/step.rs" | grep -n "leave_log2\|surface\|anchor" || sed -n '729,737p' "$ROOT/crates/universe/src/step.rs"
echo "-- universe.rs:1327 (anchor hashed into the frame digest):"
sed -n '1327p' "$ROOT/crates/universe/src/universe.rs"
echo; echo "regen done."
