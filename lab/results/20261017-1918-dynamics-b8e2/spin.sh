#!/bin/sh
# spin.sh start N   — N CPU spinners pinned to cpus 0..N-1 (pids in $SPIN_PIDFILE, default /tmp/es-spin.pids)
# spin.sh stop      — kill them
set -u
PF="${SPIN_PIDFILE:-/tmp/es-spin.pids}"
case "${1:-}" in
start)
  n=${2:-6}
  : >"$PF"
  c=0
  while [ "$c" -lt "$n" ]; do
    taskset -c "$c" sh -c 'while :; do :; done' &
    echo $! >>"$PF"
    c=$((c + 1))
  done
  echo "spinners: $(wc -l <"$PF") on cpus 0..$((n - 1)) ($PF)"
  ;;
stop)
  [ -f "$PF" ] && kill $(cat "$PF") 2>/dev/null; rm -f "$PF"
  echo "spinners stopped"
  ;;
*)
  echo "usage: spin.sh start N | spin.sh stop" >&2; exit 2 ;;
esac
