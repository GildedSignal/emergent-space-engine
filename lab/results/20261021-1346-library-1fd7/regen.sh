#!/usr/bin/env bash
# Regen: every dossier number, from a fresh Readwise fetch + the scripts + shipped code.
# Total wall time ~40 s (fetch ~6 s; scripts < 1 s). No engine patch is required for any
# number in the dossier (zero-flight composition); the tree citations grep the shipped
# files directly, so work/patch.diff (if any) changes nothing here.
set -euo pipefail
cd "$(dirname "$0")"

echo "== Fresh Readwise export (cached to readwise_cache.json)"
python3 fetch_readwise.py

echo
echo "== Quote verification (P6)"
python3 verify_quotes.py

echo
echo "== The desynchronised-grid composition (P1-P5, P7)"
python3 compose_desync.py

echo
echo "== Shipped-code citations (the adoption shape)"
grep -n "pub fn constants" ../../../crates/universe/src/ext.rs | head -1
grep -n "let want = step_for" ../../../crates/universe/src/step.rs | head -1
