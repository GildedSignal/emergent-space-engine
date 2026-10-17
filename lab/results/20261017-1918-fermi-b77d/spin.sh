#!/bin/sh
# One CPU burner, pinned if possible. Usage: spin.sh <core-id> &  (kill with the pid file)
CORE="${1:-0}"
if command -v taskset >/dev/null 2>&1; then
  taskset -c "$CORE" python3 -c 'while True: pass' &
else
  python3 -c 'while True: pass' &
fi
echo $! > "spin.$CORE.pid"
