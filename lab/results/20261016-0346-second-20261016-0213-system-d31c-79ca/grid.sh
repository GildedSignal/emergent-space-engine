#!/bin/bash
# The one-state rung (checker 2's named gold experiment on d31c): the plan pass's per-body
# recomputations of shared quantities — the body's own state (read 3x shipped: register word,
# projection, tail) and the per-doll clock constants (identical for every non-source body) —
# served once. Usage: bash grid.sh   (sequential; each flight logs to out/)
set -u
cd "$(dirname "$0")"
mkdir -p out
BIN=/home/glmlab/lab-target-3/release/examples/birth_rail
for ns in "10000 1" "10000 7" "10000 11" "30000 1" "100000 1" "100000 7" "100000 11"; do
  set -- $ns
  n=$1; seed=$2
  for arm in off on state full; do
    unset ES_PLANETS_AT_T ES_STATE_ONCE ES_CONSTANTS_ONCE
    case $arm in
      on) export ES_PLANETS_AT_T=1 ;;
      state) export ES_PLANETS_AT_T=1 ES_STATE_ONCE=1 ;;
      full) export ES_PLANETS_AT_T=1 ES_STATE_ONCE=1 ES_CONSTANTS_ONCE=1 ;;
    esac
    echo "=== N=$n seed=$seed arm=$arm ==="
    ES_BIRTH_SPLIT=1 "$BIN" "$n" "$seed" 3000 | tee "out/n${n}_s${seed}_${arm}.txt"
  done
done
# Orthogonality cell: the state lever without the planets memo (10^4 seed 1 only).
unset ES_PLANETS_AT_T ES_CONSTANTS_ONCE; export ES_STATE_ONCE=1
echo "=== N=10000 seed=1 arm=stateonly ==="
ES_BIRTH_SPLIT=1 "$BIN" 10000 1 3000 | tee "out/n10000_s1_stateonly.txt"
