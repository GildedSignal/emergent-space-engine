#!/bin/bash
# The wave × player-in-the-band experiment. Flights sequential (timing cleanliness + memory).
set -u
cd /home/glmlab/actions-runner/_work/emergent-space-engine/lab-1
OUT=lab/results/20261014-2130-quant-d7e3/out
mkdir -p "$OUT"
BIN=/home/glmlab/lab-target-1/release/examples

run () {
  local name=$1; shift
  echo "=== $name start $(date +%H:%M:%S)"
  "$@" > "$OUT/$name.txt" 2>&1
  echo "--- $name exit $? $(date +%H:%M:%S)"
  grep -E "^wave" "$OUT/$name.txt" | tail -1
}

# decisive pair first: the player in the belt band, seed 1, uncapped vs capped
run band-uncapped env -u ES_PULL_CAP $BIN/wave_band 200000 1 2.5 175 100 12
run band-capped   env ES_PULL_CAP=64 $BIN/wave_band 200000 1 2.5 175 100 12
# controls: the shipped placement (player at Home), seed 1 — digest must be 38bf's c2b834bb…
run ctl-capped   env ES_PULL_CAP=64 $BIN/wave_input 200000 plain 175 100 12
run ctl-uncapped env -u ES_PULL_CAP $BIN/wave_input 200000 plain 175 100 12
# held-out seed
run band7-uncapped env -u ES_PULL_CAP $BIN/wave_band 200000 7 2.5 175 100 12
run band7-capped   env ES_PULL_CAP=64 $BIN/wave_band 200000 7 2.5 175 100 12
echo ALL DONE $(date +%H:%M:%S)
