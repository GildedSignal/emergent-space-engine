#!/usr/bin/env bash
# Load generator: N pure-CPU spinners (awk busy loop, ~0 memory, no I/O), plus start/stop helpers.
# usage: loadgen.sh start N | stop
set -u
PIDF="$(dirname "$0")/loadpids.txt"
case "${1:-}" in
  start)
    n=$2
    : > "$PIDF"
    for _ in $(seq 1 "$n"); do
      awk 'BEGIN{for(;;){}}' >/dev/null 2>&1 &
      echo $! >> "$PIDF"
    done
    echo "started $n spinners: $(wc -l < "$PIDF") pids"
    ;;
  stop)
    if [ -f "$PIDF" ]; then xargs -r kill 2>/dev/null < "$PIDF"; rm -f "$PIDF"; fi
    pkill -f 'awk .BEGIN\{for' 2>/dev/null
    echo stopped
    ;;
esac
