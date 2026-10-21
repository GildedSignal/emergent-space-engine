#!/bin/bash
# The decisive matrix: every arm flown shipped and newsfed; digests must match run to run.
set -u
cd "$(dirname "$0")/../../.."
R=${CARGO_TARGET_DIR:-target}/release/examples/scannews2
OUT="$(dirname "$0")"
PASS=0; FAIL=0
for arm in "30000 coast 1" "30000 coast 64" "30000 burn 1" "30000 burn 8" "30000 burn 64" "3000 coast 1" "3000 coast 64"; do
  set -- $arm; N=$1; MODE=$2; D=$3
  for SCAN in 0 1; do
    TAG="${N}_${MODE}_D${D}_$([ $SCAN = 1 ] && echo newsfed || echo shipped)"
    LOG="$OUT/matrix_${TAG}.log"
    if [ "$SCAN" = 1 ]; then export SCAN_NEWSFED=1; else unset SCAN_NEWSFED; fi
    BELT_DESYNC=$D timeout 300 "$R" "$N" "$MODE" 6 100 >"$LOG" 2>&1
    grep -E "^scannews2|^SCAN2" "$LOG"
  done
  A=$(grep -oP 'digest="\K[0-9a-f]+' "$OUT/matrix_${N}_${MODE}_D${D}_shipped.log")
  B=$(grep -oP 'digest="\K[0-9a-f]+' "$OUT/matrix_${N}_${MODE}_D${D}_newsfed.log")
  if [ -n "$A" ] && [ "$A" = "$B" ]; then echo "NEUTRALITY ${N} ${MODE} D=${D}: PASS"; PASS=$((PASS+1)); else echo "NEUTRALITY ${N} ${MODE} D=${D}: FAIL ($A vs $B)"; FAIL=$((FAIL+1)); fi
done
# timing arms (SCAN_TIME=1), both modes, digest ignored for cost but printed
for arm in "30000 burn 1" "30000 coast 1"; do
  set -- $arm; N=$1; MODE=$2; D=$3
  for SCAN in 0 1; do
    TAG="time_${N}_${MODE}_$([ $SCAN = 1 ] && echo newsfed || echo shipped)"
    if [ "$SCAN" = 1 ]; then export SCAN_NEWSFED=1; else unset SCAN_NEWSFED; fi
    SCAN_TIME=1 BELT_DESYNC=$D timeout 300 "$R" "$N" "$MODE" 6 100 >"$OUT/${TAG}.log" 2>&1
    grep -E "^SCAN2" "$OUT/${TAG}.log"
  done
done
echo "neutrality: $PASS pass, $FAIL fail"
