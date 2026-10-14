#!/bin/sh
# Regenerates every number in dossier.md from shipped code + work/patch.diff (the lever stack,
# applied by the runner before this runs). ~12 min cold, ~8 min warm.
set -e
cd "$(dirname "$0")/../../.."   # repo root
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/home/glmlab/lab-target-790b}"
export ES_MAX_MEMBERS=20000
RUN="lab/results/20261014-0000-second-20261013-2252-system-ad26-790b"
mkdir -p work
cargo build --release -p xtask --features emergent-universe/prof
X="$CARGO_TARGET_DIR/release/xtask universe --bench --seconds 8 --threads 1"
# The shipped arms (baseline A/B gates on one binary): the anchor and the memo control.
ES_BASELINE_ARM=1 ES_EAGER=1 $X --members 4000 --rtf 1 --seed 1 > work/base_m4000_s1.json
ES_BASELINE_ARM=1 ES_EAGER=1 $X --members 1500 --rtf 1 --seed 1 > work/base_m1500_s1.json
ES_BASELINE_ARM=1 ES_EAGER=1 ES_ORBIT_KEYS=1 ES_ORBIT_MEMO=1 $X --members 4000 --rtf 1 --seed 1 > work/base_m4000_s1_memo.json
# The stacked arms (default paths: word fix + lazy tier; memo off).
$X --members 48 --rtf 1 --seed 1 > work/st_m48_s1.json
$X --members 400 --rtf 1 --seed 1 > work/st_m400_s1.json
$X --members 1500 --rtf 1 --seed 1 > work/st_m1500_s1.json
$X --members 1500 --rtf 1 --seed 7 > work/st_m1500_s7.json        # held-out seed
$X --members 4000 --rtf 1 --seed 1 > work/st_m4000_s1.json        # the decisive arm
$X --members 12000 --rtf 1 --seed 3 > work/st_m12000_s3.json      # held-out rung
$X --members 20000 --rtf 1 --seed 1 > work/st_m20000_s1.json      # the checker's rung
$X --members 400 --rtf 100 --seed 1 > work/st_m400_s1_r100.json   # flying pace
$X --members 1500 --rtf 100 --seed 1 > work/st_m1500_s1_r100.json # the checker's flying arm
ES_ORBIT_KEYS=1 ES_ORBIT_MEMO=1 $X --members 4000 --rtf 1 --seed 1 > work/st_m4000_s1_memo.json
# The census (ad26's, unchanged) and the regenerable endgame (reads the fresh JSONs).
python3 "$RUN/census.py" work/base_m1500_s1.json work/base_m4000_s1.json work/st_m48_s1.json \
  work/st_m400_s1.json work/st_m1500_s1.json work/st_m1500_s7.json work/st_m4000_s1.json \
  work/st_m12000_s3.json work/st_m20000_s1.json work/st_m400_s1_r100.json work/st_m1500_s1_r100.json \
  | tee "$RUN/work/census.txt"
cp work/base_m4000_s1.json work/base_m4000_s1_memo.json work/st_m4000_s1.json "$RUN/work/"
 python3 "$RUN/endgame2.py" | tee "$RUN/work/endgame.txt"
cp work/base_m*.json work/st_m*.json "$RUN/work/" 2>/dev/null || true
# The suites on the stacked default paths (word fix + lazy tier).
cargo test --release -p emergent-space -p emergent-universe 2>&1 | grep -E "test result|^error|running" \
  | tee "$RUN/work/suite.txt"
echo REGEN_DONE
