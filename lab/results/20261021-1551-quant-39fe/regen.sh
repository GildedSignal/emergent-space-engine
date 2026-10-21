#!/bin/sh
# Regenerates every dossier number. The runner applies work/patch.diff (adds
# crates/universe/examples/ktail.rs) before this runs. ~1 min, Linux x86.
set -e
cd "$(dirname "$0")/../../.."   # repo root
cargo build --release -p emergent-universe --example ktail
OUT="$(dirname "$0")/out"
mkdir -p "$OUT"
BIN=target/release/examples/ktail
[ -x "$BIN" ] || BIN=$(ls -d /home/glmlab/lab-target-*/release/examples/ktail 2>/dev/null | head -1)
# steady trickle: 20 s, rtf 100, 1e5 seeds 1-2, 3e5 seed 1  (dossier table 1)
for args in "20 100 1 48 100000" "20 100 2 48 100000" "20 100 1 48 300000"; do
  echo "== $args"; $BIN $args
done > "$OUT/decisive.txt"
# the comb window: 30 s at rtf 1000 = 30k game-s  (dossier table 2)
echo "== 30 1000 1 48 100000"; $BIN 30 1000 1 48 100000 > "$OUT/comb.txt"
cat "$OUT/decisive.txt" "$OUT/comb.txt"
