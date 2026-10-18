#!/bin/sh
# Regen run 20261018-1530-system-afff: every dossier number, from shipped code + this patch.
# Total wall: ~40 s of flight after a ~15 s warm build (cold: a few minutes for deps).
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"     # .../lab/results/20261018-1530-system-afff
ROOT="$(cd "$HERE/../../.." && pwd)"      # repo root
cd "$ROOT"
git apply --check "$HERE/work/patch.diff" 2>/dev/null && git apply "$HERE/work/patch.diff" || {
    git apply --reverse --check "$HERE/work/patch.diff" 2>/dev/null && echo "patch already applied" ||
        { echo "patch fits neither a clean nor a patched tree" >&2; exit 1; }
}
cargo build --release -p emergent-universe --example nladder 2>&1 | tail -1
BIN=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-1}/release/examples/nladder
OUT="$HERE/flights"; mkdir -p "$OUT"
# A: the shipped scene (48 members, no ladder bodies).
"$BIN" 0 coast 25 100 | grep -E "ladder:|scan_census" > "$OUT/A_shipped.txt"
# B: the crowd (600 members in the player's doll).
MEMBERS=600 "$BIN" 0 coast 25 100 | grep -E "ladder:|scan_census" > "$OUT/B_crowd600.txt"
# C: the ladder N=20000 (5,000 Home-doll locals + 15,000 star-doll belt).
"$BIN" 20000 coast 25 100 | grep -E "ladder:|scan_census" > "$OUT/C_nladder20000.txt"
cat "$OUT"/*.txt
