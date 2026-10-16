#!/usr/bin/env bash
# Regen (20261016-0346-scout-7da3): the runner applies work/patch.diff first; this builds the
# stagger example, flies the four budget-free arms, and re-derives every dossier number from the
# CSVs (census.txt). Wall ≈ 4–6 min on the lab box (8 vCPU; peak RSS 1.42 GB at 3×10⁵).
set -euo pipefail
cd "$(dirname "$0")"
ROOT=../../..
BIN="${CARGO_TARGET_DIR:-$ROOT/target}/release/examples/stagger"
[ -x "$BIN" ] || cargo build --release -p emergent-universe --example stagger

fly () {  # N on|off
  local N=$1 S=$2
  if [ "$S" = on ]; then export ES_STAGGER=1; else unset ES_STAGGER; fi
  ( cd work && "$BIN" "$N" 60 "w_${N}_${S}.csv" 1000 1000000 > "log_${N}_${S}.txt" 2>&1 )
  tail -5 "work/log_${N}_${S}.txt"
}
for arm in "100000 off" "100000 on" "300000 off" "300000 on"; do fly $arm; done
( cd work && python3 analyze.py w_100000_off.csv w_100000_on.csv w_300000_off.csv w_300000_on.csv > ../census.txt )
cat census.txt
echo REGEN-OK
