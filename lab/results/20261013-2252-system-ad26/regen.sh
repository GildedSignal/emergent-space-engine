#!/bin/sh
# Regenerates every number in dossier.md from shipped code + work/patch.diff.
# The runner applies work/patch.diff before this runs. ~4 min cold, ~1.5 min warm.
set -e
cd "$(dirname "$0")/../../.."   # repo root
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/home/glmlab/lab-target-2}"
export ES_MAX_MEMBERS=20000
RUN="lab/results/20261013-2252-system-ad26"
mkdir -p work
cargo build --release -p xtask --features emergent-universe/prof
X="$CARGO_TARGET_DIR/release/xtask universe --bench --seconds 8 --threads 1"
$X --members 48   --rtf 1   --seed 1 > work/m48_s1_r1.json
$X --members 400  --rtf 1   --seed 1 > work/m400_s1_r1.json
$X --members 1500 --rtf 1   --seed 1 > work/m1500_s1_r1.json
$X --members 4000 --rtf 1   --seed 1 > work/m4000_s1_r1.json
$X --members 1500 --rtf 1   --seed 7 > work/m1500_s7_r1.json      # held-out seed
$X --members 12000 --rtf 1  --seed 3 > work/m12000_s3_r1.json     # held-out rung
$X --members 400  --rtf 100 --seed 1 > work/m400_s1_r100.json     # flying pace
python3 "$RUN/census.py" work/m48_s1_r1.json work/m400_s1_r1.json work/m1500_s1_r1.json \
  work/m4000_s1_r1.json work/m1500_s7_r1.json work/m12000_s3_r1.json work/m400_s1_r100.json \
  | tee "$RUN/work/census.txt"
python3 "$RUN/endgame.py" | tee "$RUN/work/endgame.txt"
cp work/m*.json "$RUN/work/" 2>/dev/null || true
echo REGEN_DONE
