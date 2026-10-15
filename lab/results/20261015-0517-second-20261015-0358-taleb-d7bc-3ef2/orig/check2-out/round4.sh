#!/bin/sh
# checker2 round 4: the arms that failed on the shell bug. Each job explicit.
BIN=/home/glmlab/lab-target-1/release/examples/scan_cap
cd "$(dirname "$0")"
ES_SCAN_STANDING=4 timeout 500 "$BIN" 10000 8 1 16000 100 1 > m3-cap4-seed1.txt 2>&1 & echo "m3 pid $!"
ES_RSS_LIMIT_MB=1800 timeout 500 "$BIN" 10000 8 2 16000 100 1 > m6-off-seed2-again.txt 2>&1 & echo "m6 pid $!"
ES_SCAN_STANDING=64 ES_RSS_LIMIT_MB=1900 timeout 500 "$BIN" 300000 8 1 4000 100 1 > m4-cap64-3e5.txt 2>&1 & echo "m4 pid $!"
wait
echo ROUND4-DONE
