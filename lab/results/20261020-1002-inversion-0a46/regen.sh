#!/usr/bin/env bash
# Regen: rebuild the patched nladder, fly the anchor + 4 arms, re-run the era analysis.
# ~6 min warm (build ~10 s cached, flights 33-46 s each), well under 15 min.
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root
ROOT="$(pwd)"
RUN="$ROOT/lab/results/20261020-1002-inversion-0a46"
W="$RUN/work"
BIN=/home/glmlab/lab-target-2/release/examples/nladder

# 1. apply the instrument patch (print-only CSV + Linux footprint stub + seed arg), idempotent
if git apply --check "$W/patch.diff" 2>/dev/null; then git apply "$W/patch.diff"; else echo "patch already applied (or tree dirty) — continuing"; fi
cargo build --release -p emergent-universe --example nladder 2>&1 | tail -1
# 2. anchor: CSV off, must land in the record's 2d26/ca63 family (max 780-900 ms at 1e5 rtf 2000)
"$BIN" 100000 burn 10 2000 12 1 | grep "ladder:" | tee "$W/anchor.txt"

# 3. the four arms (decisive flights, ~40 s each)
cd "$W"
[ -s a1_burn_1e5_rtf400.csv ] || ES_FRAME_CSV=1 "$BIN" 100000 burn 150 400 12 1 > a1_burn_1e5_rtf400.csv 2>&1
[ -s a3_coast_1e5_rtf400.csv ] || ES_FRAME_CSV=1 "$BIN" 100000 coast 150 400 12 1 > a3_coast_1e5_rtf400.csv 2>&1
[ -s a2_burn_15e4_rtf400.csv ] || ES_FRAME_CSV=1 "$BIN" 150000 burn 120 400 12 1 > a2_burn_15e4_rtf400.csv 2>&1
[ -s a4_burn_1e5_seed2.csv  ] || ES_FRAME_CSV=1 "$BIN" 100000 burn 150 400 12 2 > a4_burn_1e5_seed2.csv 2>&1

# 4. era analysis (the dossier's tables regenerate here)
python3 eras.py a1_burn_1e5_rtf400.csv 100028  "A1 1e5 burn seed1"
python3 eras.py a3_coast_1e5_rtf400.csv 100028 "A3 1e5 coast seed1"
python3 eras.py a2_burn_15e4_rtf400.csv 150028 "A2 1.5e5 burn seed1"
python3 eras.py a4_burn_1e5_seed2.csv  100028 "A4 1e5 burn seed2"
echo "regen done"
