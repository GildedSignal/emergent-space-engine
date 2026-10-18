#!/bin/sh
# Regen run 20261018-1617-second-...-687c: every dossier number, from shipped code + this run's
# patch (the author's census, extended with the swept metric, the window-membership record tests
# and the churn counters). Total wall: ~35 s of flight after a ~15 s warm build (cold: minutes).
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"     # .../lab/results/20261018-1617-second-20261018-1530-system-afff-687c
ROOT="$(cd "$HERE/../../.." && pwd)"      # repo root
cd "$ROOT"
git apply --check "$HERE/work/patch.diff" 2>/dev/null && git apply "$HERE/work/patch.diff" || {
    git apply --reverse --check "$HERE/work/patch.diff" 2>/dev/null && echo "patch already applied" ||
        { echo "patch fits neither a clean nor a patched tree" >&2; exit 1; }
}
cargo build --release -p emergent-universe --example nladder 2>&1 | tail -1
BIN=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-1}/release/examples/nladder
OUT="$HERE/flights"; mkdir -p "$OUT"
# A: the shipped scene (48 members); C: the ladder N=20000 (continuity with 20261018-1530-system-afff).
"$BIN" 0 coast 25 100 | grep -E "scene:|ladder:|scan_census" > "$OUT/A_shipped.txt"
"$BIN" 20000 coast 25 100 | grep -E "scene:|ladder:|scan_census" > "$OUT/C_ladder20000.txt"
# The checker's three named regimes, both seeds where it flew them.
MEMBERS=600 "$BIN" 0 coast 25 100 | grep -E "scene:|ladder:|scan_census" > "$OUT/B1_crowd600_seed1.txt"
SEED=2 MEMBERS=600 "$BIN" 0 coast 25 100 | grep -E "scene:|ladder:|scan_census" > "$OUT/B2_crowd600_seed2.txt"
MEMBERS=600 "$BIN" 0 burn 25 100 | grep -E "scene:|ladder:|scan_census" > "$OUT/BU1_crowd600_burn_seed1.txt"
# The compound regime (the record's worst ordinary case): burn inside the dense crowd.
MEMBERS=6000 "$BIN" 0 burn 25 100 | grep -E "scene:|ladder:|scan_census" > "$OUT/DB_crowd6000_burn_seed1.txt"
cat "$OUT"/*.txt
