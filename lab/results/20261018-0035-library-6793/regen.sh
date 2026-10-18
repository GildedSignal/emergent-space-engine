#!/usr/bin/env bash
# regen.sh — regenerates every number in dossier.md for 20261018-0035-library-6793.
# No flight (fermi-lens precedent: `nladder` does not link on Linux); the numbers are
# compositions of published measured constants + a fresh Readwise export.
# Wall time: ~10 s (the Readwise fetch is the only network call).
set -euo pipefail
cd "$(dirname "$0")"

# 1. Fresh Readwise export (P2's held-out property: the quotes verify against a NEW
#    fetch, not the author's cache). Cached copy is kept as work/highlights.json.bak.
if [ -n "${READWISE_TOKEN:-}" ]; then
  mv -f work/highlights.json work/highlights.json.bak 2>/dev/null || true
  python3 verify_quotes.py work/highlights.json | tee work/quotes_fresh.txt
else
  echo "READWISE_TOKEN unset — verifying against the author's cached fetch" >&2
  python3 verify_quotes.py | tee work/quotes_fresh.txt
fi

# 2. The composed 10^9 memory table and the prediction checks P1/P3/P4/P5.
python3 compose_mem.py | tee work/compose_out.txt

# 3. Grounding greps cited by the dossier (the Binding anatomy and the scar shelf,
#    the two shipped structures behind the plateau and the store's ladder).
{
  ROOT="$(cd ../../.. && pwd)"
  echo "--- crates/universe/src/bind.rs: pub struct Binding (the 192 B measured by memory-h-live)"
  grep -n "pub struct Binding" "$ROOT/crates/universe/src/bind.rs"
  echo "--- crates/shipmem/src/shelf.rs: the scar shelf (the store's compact ladder)"
  grep -n "seals them as scars\|pub scars" "$ROOT/crates/shipmem/src/shelf.rs"
} > work/grounding.txt 2>&1 || true
cat work/grounding.txt

echo "REGEN OK — dossier numbers: Table 1 + P1/P3/P4/P5 in work/compose_out.txt; quotes in work/quotes_fresh.txt"
