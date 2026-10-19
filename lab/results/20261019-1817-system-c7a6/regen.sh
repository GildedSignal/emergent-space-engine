#!/bin/sh
# Regenerates every number in dossier.md from the shipped tree + this run's patch.
# The patch (work/patch.diff: the read census instrument, the Linux footprint, the probe line in
# nladder) is applied by the runner before this runs. Three flights of ~60 s wall + analysis.
set -e
cd "$(dirname "$0")/../../.." || exit 1
BIN=${BIN:-/home/glmlab/lab-target-3/release/examples/nladder}
OUT=lab/results/20261019-1817-system-c7a6/work
mkdir -p "$OUT"
cargo build --release -p emergent-universe --example nladder -j 6
# A — the ratchet scene, headless (the view never gathers in flight): the demand side.
READ_CENSUS=1 LADDER_CAP_S=100 "$BIN" 30000 burn 100 2000 > "$OUT/armA_burn.log" 2>&1
# B — the view gathers every 15 s of wall time: the view's own demand (retarded crossings).
READ_CENSUS=1 LADDER_CAP_S=100 LADDER_VIEW_EVERY=900 "$BIN" 30000 burn 100 2000 > "$OUT/armB_view.log" 2>&1
# C — coast control at the same rung: the demand with no recession.
READ_CENSUS=1 LADDER_CAP_S=100 "$BIN" 30000 coast 100 2000 > "$OUT/armC_coast.log" 2>&1
for a in armA_burn armB_view armC_coast; do
  echo "== $a"
  python3 "$OUT/census_sum.py" "$OUT/$a.log" | tee "$OUT/$a.sum"
done
echo "regen done; the dossier's numbers are in $OUT/*.sum and the logs beside them."
