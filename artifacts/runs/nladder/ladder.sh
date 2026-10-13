#!/bin/sh
# The N ladder's runs: one process a rung and flight (each <= 60 s of wall, build included), machine state recorded before each.
# Usage: ladder.sh <plain binary> <prof binary> <out dir> [rungs] [prof rungs]
# Needs the two binaries of `cargo build --release -p emergent-universe [--features prof] --example nladder`, copied apart.
PLAIN="$1"; PROF="$2"; OUT="$3"; RUNGS="${4:-0 100 1000 10000 100000 1000000}"; PRUNGS="${5:-0 1000 10000 100000}"
cd "$(dirname "$0")/../../.." || exit 1
mkdir -p "$OUT"
for n in $RUNGS; do
  for fl in coast burn; do
    {
      ./artifacts/runs/frame/state.sh
      "$PLAIN" "$n" "$fl" 20
    } > "$OUT/n${n}_${fl}.txt" 2>&1
  done
done
for n in $PRUNGS; do
  for fl in coast burn; do
    {
      ./artifacts/runs/frame/state.sh
      "$PROF" "$n" "$fl" 20
    } > "$OUT/prof_n${n}_${fl}.txt" 2>&1
  done
done
./artifacts/runs/frame/state.sh > "$OUT/state_end.txt"
