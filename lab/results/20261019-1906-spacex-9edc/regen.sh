#!/bin/sh
# Regenerates every dossier number from the shipped tree + work/patch.diff (applied before this runs).
# Builds once (~1 min warm), then three flights (~50 s wall each) + one 20-s arm. Total ~5 min.
set -e
cd "$(dirname "$0")/../../.." || exit 1
BIN="${CARGO_TARGET_DIR:-/home/glmlab/lab-target-3}/release/examples/nladder"
cargo build --release -p emergent-universe --example nladder 2>&1 | tail -1
OUT=lab/results/20261019-1906-spacex-9edc/work
mkdir -p "$OUT"
# A: the decisive arm (seed 1, 10^4, coast, rtf 1800): belt waves + locals' tube stream.
ES_KICK_NEWS=1 "$BIN" 10000 coast 150 1800 2>&1 | grep -E "ladder:|kicknews:" > "$OUT/armA.txt"
# B: held-out seed 2.
ES_KICK_NEWS=1 ES_LADDER_SEED=2 "$BIN" 10000 coast 150 1800 2>&1 | grep -E "ladder:|kicknews:" > "$OUT/armB.txt"
# C: the second rung, 3x10^4.
ES_KICK_NEWS=1 "$BIN" 30000 coast 150 1800 2>&1 | grep -E "ladder:|kicknews:" > "$OUT/armC.txt"
# D: flag-off control (census must read zero; ladder digits inside the load spread).
"$BIN" 10000 coast 150 1800 2>&1 | grep -E "ladder:|kicknews:" > "$OUT/armD_off.txt"
# E: the 20-s arm (never reaches the belt's first wave: the locals-only negative control).
ES_KICK_NEWS=1 "$BIN" 10000 coast 20 100 2>&1 | grep -E "ladder:|kicknews:" > "$OUT/armE_short.txt"
echo "--- armA"; cat "$OUT/armA.txt"; echo "--- armB"; cat "$OUT/armB.txt"
echo "--- armC"; cat "$OUT/armC.txt"; echo "--- armD (off)"; cat "$OUT/armD_off.txt"
echo "--- armE (short)"; cat "$OUT/armE_short.txt"
