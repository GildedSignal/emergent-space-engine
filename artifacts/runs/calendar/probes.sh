#!/bin/sh
# The calendar job's probes, one at a time (each <= 60 s of wall), the machine state recorded with each: the N ladder at
# N = 0, 10^5, 10^6, coasting and burning at L8, for 200 s and 20 s (the schedule's bytes, the hot set, the frames' event load),
# and the grid probe at 10^4 over game days.
# Usage: probes.sh <nladder binary> <grid binary> <out dir>
NL="$1"; GR="$2"; OUT="$3"
cd "$(dirname "$0")/../../.." || exit 1
./artifacts/runs/cadence/ladder200.sh "$NL" "$OUT/s200" "0 100000 1000000" 200
./artifacts/runs/cadence/ladder200.sh "$NL" "$OUT/s20" "0 100000 1000000" 20
{ ./artifacts/runs/frame/state.sh; "$GR" 10000 1e6; } > "$OUT/grid_n10000.txt" 2>&1
