#!/bin/sh
# Regenerates every number in the dossier: builds the probe (from work/patch.diff, applied by the
# runner before this runs) and runs the nose-map grid plus the boundary re-run. ~6-10 minutes.
set -e
cd "$(dirname "$0")/../.."
cargo build --release -p emergent-universe --example nose_map -p emergent-universe --example turn_probe
BIN=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-2}/release/examples/nose_map
cd lab/results/20261013-0459-taleb-9cb7/work
"$BIN" 16 0,2,4,6,8,10,12,15 10 36 > grid.out 2> grid.err
"$BIN" 16 6 10 36 > refine.out 2> refine.err
python3 summarize.py
