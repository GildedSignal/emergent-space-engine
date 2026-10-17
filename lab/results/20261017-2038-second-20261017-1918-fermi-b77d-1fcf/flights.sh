#!/bin/bash
# The crowd rung: K in {1000,1600,2400,4000,10000} x {quiet, loaded(7 spinners)},
# paced player loop, pin in real bytes (counting GlobalAlloc inside the example).
# Each flight self-truncates at 55 s; LIVE_GUARD_B stops it before live allocs pass 1.3 GB.
set -u
RUN="$(cd "$(dirname "$0")" && pwd)"
BIN="${1:-${CARGO_TARGET_DIR:-$RUN/../../../target}/release/examples/flowcrowd}"
BIN="$(readlink -f "$BIN")"
[ "$#" -gt 0 ] && shift
OUT="${1:-$RUN/flights}"
[ "$#" -gt 0 ] && shift
mkdir -p "$OUT"
KS="${*:-1000 1600 2400 4000 10000}"
SPIN_CORES="1 2 3 4 5 6 7"

spin_up() {
  for c in $SPIN_CORES; do
    taskset -c "$c" python3 -c 'while True: pass' >/dev/null 2>&1 &
    echo $! >> "$OUT/spin.pids"
  done
  sleep 1
}
spin_down() {
  if [ -f "$OUT/spin.pids" ]; then kill $(cat "$OUT/spin.pids") 2>/dev/null; rm -f "$OUT/spin.pids"; fi
  sleep 1
}
trap spin_down EXIT

for K in $KS; do
  for mode in q l; do
    name="K${K}${mode}"
    if [ "$mode" = l ]; then spin_up; else spin_down; fi
    echo "=== arm $name (MEMBERS=$K) $(date +%H:%M:%S) loadavg=$(cat /proc/loadavg) ==="
    timeout 75 env MEMBERS="$K" LIVE_GUARD_B=1300000000 "$BIN" 50 100 > "$OUT/$name.log" 2>&1
    echo "--- $name exit=$? loadavg=$(cat /proc/loadavg); summary: $(grep '^summary' "$OUT/$name.log" | tail -1)"
    if [ "$mode" = l ]; then spin_down; fi
  done
done

# the unpaced no-gather arms (the pin isolated from the view's cost at the top of the range;
# the paced K=1e4 loop never reaches the FLOW — the view crawls at ~74 ms/frame there)
spin_down
for K in 4000 10000; do
  name="K${K}u"
  echo "=== arm $name (MEMBERS=$K UNPACED no per-frame gather) $(date +%H:%M:%S) loadavg=$(cat /proc/loadavg) ==="
  timeout 75 env MEMBERS="$K" UNPACED=1 GATHER_EVERY=1000000000 LIVE_GUARD_B=1300000000 "$BIN" 50 100 > "$OUT/$name.log" 2>&1
  echo "--- $name exit=$? loadavg=$(cat /proc/loadavg); summary: $(grep '^summary' "$OUT/$name.log" | tail -1)"
done
