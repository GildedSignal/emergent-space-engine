#!/bin/bash
# regen.sh — 20261021-1551-second-20261021-1443-system-9b03-89f3
# Regenerates every number in dossier.md from shipped code + work/patch.diff.
# Wall: about 2 minutes (one build ~15 s, 16 deterministic flights, 25 s together).
set -e
cd "$(dirname "$0")/../../.."   # repo root
git apply "$(dirname "$0")/work/patch.diff" 2>/dev/null || echo "(patch already applied)"
cargo build --release -p emergent-universe --example scannews2
R=${CARGO_TARGET_DIR:-target}/release/examples/scannews2
OUT="$(dirname "$0")"

# The digest-neutrality matrix + the dial sweep (the dossier's tables 1 and 2).
bash "$OUT/runmatrix.sh"

# The exactness cross-check at a second horizon (20 s wall, coast): digest must still match.
for SCAN in 0 1; do
  if [ "$SCAN" = 1 ]; then export SCAN_NEWSFED=1; else unset SCAN_NEWSFED; fi
  BELT_DESYNC=1 timeout 300 "$R" 30000 coast 20 100 >"$OUT/horizon20_$SCAN.log" 2>&1
  grep -E "^scannews2|^SCAN2" "$OUT/horizon20_$SCAN.log"
done
A=$(grep -oP 'digest="\K[0-9a-f]+' "$OUT/horizon20_0.log"); B=$(grep -oP 'digest="\K[0-9a-f]+' "$OUT/horizon20_1.log")
[ -n "$A" ] && [ "$A" = "$B" ] && echo "NEUTRALITY 30000 coast 20s horizon: PASS" || echo "NEUTRALITY 30000 coast 20s horizon: FAIL ($A vs $B)"

# The steady-state cost attribution at 193 scans (the dossier's coast 20 s timed row: the 6 s
# figure's +52 us is the one-time 30k-slot cache build; this run shows the steady +23 us).
for SCAN in 0 1; do
  if [ "$SCAN" = 1 ]; then export SCAN_NEWSFED=1; else unset SCAN_NEWSFED; fi
  SCAN_TIME=1 BELT_DESYNC=1 timeout 300 "$R" 30000 coast 20 100 >"$OUT/time20_$SCAN.log" 2>&1
  grep -E "^SCAN2" "$OUT/time20_$SCAN.log"
done
echo "regen done"
