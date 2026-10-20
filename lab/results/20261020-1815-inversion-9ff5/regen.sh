#!/bin/bash
# Regen (run 20261020-1815-inversion-9ff5): rebuilds the longflight instrument (a new
# example file, print-only relative to the shipped nladder loop; no engine change) and
# reflies the control, the 34-era long flight and the seed-2 arm, then both analyses
# (fixed-window = the shear lesson; era-binned = the honest read). ~7 min on the lab box.
set -e
cd "$(dirname "$0")/../../.."   # repo root
OUT="$(dirname "$0")/work"
mkdir -p "$OUT"
cargo build --release -p emergent-universe --example longflight 2>&1 | tail -1
BIN=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-3}/release/examples/longflight
# C0: control, 4.3 eras (anchors onset, arrivals, first-era mint against the record)
"$BIN" 50000 coast 75 1800 > "$OUT/control-c0.csv" 2> "$OUT/control-c0.err"
# A1: the decisive long flight, 34.2 eras (556 s of frames)
"$BIN" 50000 coast 556 1800 > "$OUT/long-a1.csv" 2> "$OUT/long-a1.err"
# S2: seed-2 robustness arm, 5.6 eras
ES_SEED=2 "$BIN" 50000 coast 100 1800 > "$OUT/seed2-s2.csv" 2> "$OUT/seed2-s2.err"
echo "== C0 (era bins) =="; python3 "$(dirname "$0")/eras.py" "$OUT/control-c0.csv" 50028
echo "== A1 fixed windows (the shear lesson) =="; python3 "$(dirname "$0")/analyze.py" "$OUT/long-a1.csv" 50028
echo "== A1 era bins (the honest read) =="; python3 "$(dirname "$0")/eras.py" "$OUT/long-a1.csv" 50028
echo "== S2 era bins =="; python3 "$(dirname "$0")/eras.py" "$OUT/seed2-s2.csv" 50028
tail -1 "$OUT/control-c0.err"; tail -1 "$OUT/long-a1.err"; tail -1 "$OUT/seed2-s2.err"
