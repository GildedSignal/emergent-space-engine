#!/bin/sh
# Cadence sweep: B12-B14, B17 on the motion-law-v2 plane at --plane-step N.
# PLANE_TRACE leaves event counts on stderr; captured per line.
cd /home/glmlab/actions-runner/_work/emergent-space-engine/lab-3
XT=/home/glmlab/lab-target-3/release/xtask
OUT=lab/results/20261011-0836-spacex-0c44/work/sweep.log
: > "$OUT"
for gate in B13 B14 B12 B17; do
  for n in 7 6 5 4 3 2 1; do
    echo "=== $gate step $n ===" >> "$OUT"
    start=$(date +%s.%N)
    PLANE_TRACE=1 timeout 120 "$XT" behave --law plane --gates "$gate" --plane-step "$n" \
      >> "$OUT" 2>> "$OUT.trace" || echo "EXIT=$? (timeout/fail)" >> "$OUT"
    end=$(date +%s.%N)
    echo "wall=$(echo "$end $start" | awk '{printf "%.1f", $1-$2}')s" >> "$OUT"
  done
done
echo DONE >> "$OUT"
