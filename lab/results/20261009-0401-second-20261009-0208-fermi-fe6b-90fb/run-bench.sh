#!/bin/bash
# The checker's named experiment: anchor the kick->cascade at N >= 1e6 on the shipped
# code, plus the program-level event-queue churn. Single-threaded timed loops (as shipped).
# Reproduce: bash run-bench.sh   (builds are cached; ~3 min on the shared runner)
set -u
cd "$(dirname "$0")"
OUT=cascade.jsonl
B=/tmp/lab-target-90fb/release/cascade-bench
( cd bench && CARGO_TARGET_DIR=/tmp/lab-target-90fb cargo build --release ) || exit 1
: > $OUT

echo "== state: $(date -u +%FT%TZ) load: $(cut -d' ' -f1-3 /proc/loadavg)" | tee -a $OUT

# 0) Shipped anchor: the r8-lineage kick experiment, current code, its own n=1e4 spec.
CARGO_TARGET_DIR=/tmp/lab-target-90fb-ws cargo run --release -p emergent-encounters -- kick 2>err-anchor.txt | tee -a $OUT

# 1) Global Sorted ladder (shipped index path). rho: dilute = 1e-4*1e4/n at fixed extent;
#    grown extent keeps the anchor's local density (rho, sigma_e unchanged).
$B global a4    10000 1e-2 1e-4 1 1.5    100 | tee -a $OUT
$B global g5w  100000 1e-2 1e-5 1 1.5     20 | tee -a $OUT
$B global g5W  100000 1e-2 1e-4 1 15      20 | tee -a $OUT
$B global g6w 1000000 1e-2 1e-6 1 1.5     20 | tee -a $OUT
$B global g6W 1000000 1e-2 1e-4 1 150     30 | tee -a $OUT
$B global g6Wd 1000000 1e-2 1e-4 1 15     30 | tee -a $OUT
# Optional 1e7 point (X=1500): exceeded 300 s/kick on the loaded shared runner; the
# law row in budget.py extrapolates it (1.7e5 pairs/kick). Uncomment on a quiet machine:
# $B global g7W 10000000 1e-2 1e-4 1 1500   10 | tee -a $OUT

# 2) Cell-local index (geometric equal-count blocks, per-block Sorted, sound union bounds),
#    with the exact same-lagged-bodies soundness control (set equality, no sampling).
$B cells  c6W  1000000 1e-2 1e-4 1 150 100 30 | tee -a $OUT
$B cells  c6Wd 1000000 1e-2 1e-4 1 15  100 30 | tee -a $OUT
$B verify 100000 1e-2 1e-4 1 15  10 30         | tee -a $OUT
$B verify 1000000 1e-2 1e-4 1 150 100 30       | tee -a $OUT

# 3) Event-queue churn at the program-level key count (1e9/128 = 7.8e6) and at 2e6.
$B heap 7800000 3000000 | tee -a $OUT
$B heap 2000000 3000000 | tee -a $OUT

echo "== state: $(date -u +%FT%TZ) load: $(cut -d' ' -f1-3 /proc/loadavg)" | tee -a $OUT
