#!/bin/bash
# The birth rail's shared-readout rung: one shared "planets at t" readout for both read paths.
# Usage: bash grid.sh   (sequential; each flight logs to out/)
set -u
cd "$(dirname "$0")"
mkdir -p out
BIN=/home/glmlab/lab-target-3/release/examples/birth_rail
for ns in "10000 1" "10000 7" "10000 11" "30000 1" "100000 1" "100000 7" "100000 11"; do
  set -- $ns
  n=$1; seed=$2
  for arm in off on; do
    if [ "$arm" = off ]; then unset ES_PLANETS_AT_T; else export ES_PLANETS_AT_T=1; fi
    echo "=== N=$n seed=$seed memo=$arm ==="
    ES_BIRTH_SPLIT=1 "$BIN" "$n" "$seed" 3000 | tee "out/n${n}_s${seed}_${arm}.txt"
  done
done
