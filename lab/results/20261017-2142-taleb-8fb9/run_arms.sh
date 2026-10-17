#!/bin/bash
# 20261017-2142-taleb-8fb9: the battalion census arm suite. One flight per arm, N=100000, 5 fire windows.
# Usage: run_arms.sh <outdir> [binary]
set -u
OUT="$1"; BIN="${2:-/home/glmlab/lab-target-1/release/examples/belt_comb}"
mkdir -p "$OUT"
# the machine's state, recorded with the run (PRINCIPLES: measure the way the player runs it)
{ date; uname -r; nproc; cat /proc/loadavg; grep MemAvailable /proc/meminfo; } > "$OUT/machine.txt"
N=100000; W=5
run() { # name seed a_shift p_shift
  local name=$1 seed=$2 a=$3 p=$4
  echo "=== $name (seed $seed, a_shift=$a, p_shift=$p) start $(date +%T)" >> "$OUT/arms.log"
  ES_BELT_A_SHIFT=$a ES_BELT_PHASE_SHIFT=$p "$BIN" $N $W $seed > "$OUT/$name.txt" 2>&1
  echo "=== $name exit=$? end $(date +%T)" >> "$OUT/arms.log"
}
run ctrl    1 0  0
run per     1 27 0
run phase   1 0  8
run both384 1 28 2
run both96  1 29 1
run both48  1 30 1
run anchor100 1 30 30
run anchor200 1 30 29
run ctrl_s7   7 0  0
run both96_s7 7 29 1
echo DONE >> "$OUT/arms.log"
