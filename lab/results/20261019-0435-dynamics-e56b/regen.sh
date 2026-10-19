#!/bin/bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff.
# Applies the patch (adds crates/lattice/examples/fleetburst.rs), builds offline,
# flies the 15-flight grid plus the long 6400 horizon, and runs both analyzers.
set -eu
cd "$(dirname "$0")"          # the run folder
cd ../../..                   # repo root
if [ -f lab/results/20261019-0435-dynamics-e56b/work/patch.diff ] && [ ! -f crates/lattice/examples/fleetburst.rs ]; then
  git apply lab/results/20261019-0435-dynamics-e56b/work/patch.diff
fi
cargo build -p emergent-lattice --release --offline --example fleetburst 2>&1 | tail -1
cd lab/results/20261019-0435-dynamics-e56b
./run_grid.sh
BIN=${BIN:-/home/glmlab/lab-target-3/release/examples/fleetburst}
$BIN --scene mixed --n 6400 --boxscale 2 --nojitter --horizon 24576 --seed 1 --out work/mb6400_bs2_s1_long.tsv 2>/dev/null
# determinism spot-check (digest must equal the stored flight's)
$BIN --scene mixed --n 1600 --boxscale 2 --nojitter --horizon 16384 --seed 1 --out /tmp/regen_mb1600.tsv 2>/dev/null
a=$(grep -o 'digest=.*' /tmp/regen_mb1600.tsv); b=$(grep -o 'digest=.*' work/mb1600_bs2_s1.tsv)
[ "$a" = "$b" ] && echo "DETERMINISM_OK $a" || { echo "DETERMINISM_FAIL"; exit 1; }
python3 analyze.py > work/table.txt
python3 analyze2.py > work/final_print.txt
echo REGEN_DONE
