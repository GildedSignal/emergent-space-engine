#!/bin/sh
# Regenerates the growth finding: one 10^4 coast arm at rtf 6000 / 12 ms budget, RSS sampled
# every 10 s from /proc, killed at the 2 GB ceiling (the run's survival rule). The arm never
# reaches its 20 s of frames; the growth curve is the number.
B=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-2}/release/examples/nladder_lin
cd "$(dirname "$0")"
"$B" 10000 coast 20 6000 12 > growth_flight.txt 2>&1 &
PID=$!
i=0
while kill -0 $PID 2>/dev/null; do
  rss=$(awk '/VmRSS/{print $2}' /proc/$PID/status 2>/dev/null)
  echo "t=$((i*10))s rss_kb=$rss"
  [ -n "$rss" ] && [ "$rss" -gt 1900000 ] && break
  sleep 10; i=$((i+1))
  [ $i -ge 30 ] && break
done
kill -9 $PID 2>/dev/null
cat growth_flight.txt
echo GROWTH_DONE
