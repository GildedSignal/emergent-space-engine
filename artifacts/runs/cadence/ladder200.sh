#!/bin/sh
# N1 sustained: the N ladder's probe with 200 s flights (coast and the L8 burn), one process a rung and flight (each <= 60 s of
# wall, build included: the probe cuts itself at 55 s and says "truncated"), the machine state recorded before each.
# Usage: ladder200.sh <nladder binary> <out dir> [rungs] [seconds]
BIN="$1"; OUT="$2"; RUNGS="${3:-1000 10000 100000 300000 500000 1000000}"; SECS="${4:-200}"
cd "$(dirname "$0")/../../.." || exit 1
mkdir -p "$OUT"
for n in $RUNGS; do
  for fl in coast burn; do
    {
      ./artifacts/runs/frame/state.sh
      "$BIN" "$n" "$fl" "$SECS"
    } > "$OUT/n${n}_${fl}.txt" 2>&1
  done
done
./artifacts/runs/frame/state.sh > "$OUT/state_end.txt"
