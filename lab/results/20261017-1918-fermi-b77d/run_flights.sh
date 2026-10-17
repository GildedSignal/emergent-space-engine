#!/bin/bash
# The FLOW-under-load arms. Each flight ≤ 60 s (nladder self-truncates at 55 s).
# Usage: run_flights.sh <binary> <outdir> [arm ...]
set -u
BIN="${1:-./target/release/examples/nladder}"
OUT="${2:-$(dirname "$0")/flights}"
mkdir -p "$OUT"
ARMS="${*:-A1 A2 B1 B2 C}"
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
fly() { # name seconds members n
  local name="$1" secs="$2" mem="$3" n="$4"
  echo "=== arm $name (MEMBERS=$mem N=$n) $(date +%H:%M:%S) loadavg=$(cat /proc/loadavg) ==="
  timeout 75 env MEMBERS="$mem" "$BIN" "$n" coast "$secs" 100 12 > "$OUT/$name.log" 2>&1
  echo "--- $name exit=$? tail:"; tail -3 "$OUT/$name.log"
}
trap spin_down EXIT

for arm in $ARMS; do
  case "$arm" in
    A1) spin_down; fly A1 50 400 0 ;;
    A2) spin_up;   fly A2 50 400 0; spin_down ;;
    B1) spin_down; fly B1 50 48 100000 ;;
    B2) spin_up;   fly B2 50 48 100000; spin_down ;;
    B3) spin_down; fly B3 50 48 10000 ;;
    C)  spin_up;   fly C  50 1000 0; spin_down ;;
    C1) spin_down; fly C1 50 1000 0 ;;
  esac
done
