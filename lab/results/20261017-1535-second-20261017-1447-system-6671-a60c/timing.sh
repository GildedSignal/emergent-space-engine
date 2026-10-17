#!/bin/sh
# The timing matrix: {10^4,10^5} x {coast,burn} x {memo off,on}, interleaved A/B x 3 reps.
# Medians over reps decide (shared box); the ladder: line carries p50/p99/max ms and wall_s;
# the memo: line carries the flight's own hit rate and live-key high-water.
set -e
cd "$(dirname "$0")/../../.." >/dev/null 2>&1 || cd "$(pwd)"
OUT=lab/results/20261017-1535-second-20261017-1447-system-6671-a60c
BIN=${CARGO_TARGET_DIR:-target}/release/examples/nladder
for n in 10000 100000; do
  for flight in coast burn; do
    rm -f "$OUT/timing-n${n}-${flight}.txt"
    for rep in 1 2 3; do
      for arm in off on; do
        if [ "$arm" = on ]; then export ES_MEMO=1 ES_MEMO_STATS=1; else unset ES_MEMO ES_MEMO_STATS; fi
        echo "== n=$n $flight rep=$rep arm=$arm ==" >> "$OUT/timing-n${n}-${flight}.txt"
        $BIN $n $flight 60 600 2>&1 | grep -E "^ladder: |^memo: |^game " >> "$OUT/timing-n${n}-${flight}.txt"
      done
    done
  done
done
unset ES_MEMO ES_MEMO_STATS
echo done
