#!/bin/bash
set -u
cd /home/glmlab/actions-runner/_work/emergent-space-engine/lab-1
OUT=lab/results/20261014-2130-quant-d7e3/out
BIN=/home/glmlab/lab-target-1/release/examples
run () { local name=$1; shift; echo "=== $name $(date +%H:%M:%S)"; /usr/bin/time -v "$@" > "$OUT/$name.txt" 2>&1; echo "exit $? $(date +%H:%M:%S)"; grep -E "Maximum resident" "$OUT/$name.txt"; grep -E "^wave" "$OUT/$name.txt" | tail -1; }
run band50-uncapped env -u ES_PULL_CAP $BIN/wave_band 50000 1 2.5 155 100 12
run band50-capped   env ES_PULL_CAP=64 $BIN/wave_band 50000 1 2.5 155 100 12
run band100-capped  env ES_PULL_CAP=64 $BIN/wave_band 100000 1 2.5 175 100 12
echo DONE2 $(date +%H:%M:%S)
