#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped code + this folder's scripts.
# work/patch.diff (the promo_contact example) is applied by the runner before this runs.
# Total ~6-8 min: dumper build ~1 min, dump 30-90 s, bench build ~2 min, bench 30 s.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
cd "$ROOT"

echo "== 1. regenerate the measured encounter dump from the shipped encounters crate =="
# c7eb's dumper verbatim (path-depends on the unmodified crate), game3d belt:
# n=2000, sigma_e=0.1, rho=1e-4 AU, a in [2.45,2.95], 50 orbits, seed 20261009.
(cd "$HERE/dumper" && cargo run --release --quiet -- game3d "$HERE/game3d-regen" 30) > "$HERE/dump-regen.log" 2>&1
if diff -q "$HERE/game3d-regen-enc.jsonl" "$HERE/game3d-enc.jsonl" >/dev/null; then
  echo "DUMP regen: bit-identical to the stored record (482 encounters)"
else
  echo "DUMP regen: DIFFERS from the stored record (truth nondeterminism?)" >&2
  diff "$HERE/game3d-regen-enc.jsonl" "$HERE/game3d-enc.jsonl" | head -5 >&2
fi

echo "== 2. regenerate triples.rs (the bench includes it at compile time) =="
python3 "$HERE/extract.py" "$HERE/game3d-regen-enc.jsonl" "$HERE/triples.rs"

echo "== 3. build + run the bench (cold, eccentric, far band; ~30 s) =="
touch crates/shipmem/examples/promo_contact.rs  # include! files are not fingerprinted
cargo build --release --quiet -p emergent-shipmem --example promo_contact
cargo run --release --quiet -p emergent-shipmem --example promo_contact \
  > "$HERE/run.log" 2>&1
grep -E "^(BELT|MASS|COMPOSED|FAR|STAT FAR|STATE)" "$HERE/run.log" | head -40
echo "REGEN OK — full record in $HERE/run.log"
