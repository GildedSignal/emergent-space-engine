#!/bin/sh
# Regen for 20261013-0236-inversion-57ce (the E->1 in-flight crossing grid + capture probe).
# work/patch.diff adds crates/universe/examples/crossing.rs (applied by the runner before this runs).
# Total wall on the lab's shared x86 runner: ~5 minutes.
set -e
cd "$(dirname "$0")/../../.."   # repo root
cargo build --release -p emergent-universe --example crossing
B=${CARGO_TARGET_DIR:-target}/release/examples/crossing
OUT=lab/results/20261013-0236-inversion-57ce/out
mkdir -p "$OUT"
for L in 15 11 8 5 4 3 2; do
  timeout 120 "$B" A$L 30000 > "$OUT/A$L.txt" 2>&1 || true
  echo "== A$L (rc=$?)"
done
timeout 240 "$B" B8 40000 > "$OUT/B8.txt" 2>&1 || true
echo "== B8 (rc=$?)"
echo "--- crossing brackets (kind flips):"
grep -h -- "-lo \|-up " "$OUT"/A*.txt "$OUT"/B8.txt || true
echo "--- deaths:"
grep -h "DEAD" "$OUT"/A*.txt "$OUT"/B8.txt || true
echo "--- ladder ends / captures:"
grep -h "ladder ends\|cap\b\|capcoast\|bcoast\|no capture\|done" "$OUT"/A*.txt "$OUT"/B8.txt || true
