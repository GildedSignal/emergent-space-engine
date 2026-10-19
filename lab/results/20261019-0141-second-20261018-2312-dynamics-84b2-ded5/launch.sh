#!/bin/sh
# Detached launcher for the decisive arms (survives the calling shell).
B=/home/glmlab/lab-target-1/release/examples/breathe
D="$(cd "$(dirname "$0")" && pwd)/data"
cd "$D" || exit 1
setsid nohup "$B" 12800 0.7 65536 2 1024 24576 0 > ext_n12800_s2.csv 2> ext_n12800_s2.err < /dev/null &
setsid nohup "$B" 12800 0.7 65536 3 1024 24576 0 > ext_n12800_s3.csv 2> ext_n12800_s3.err < /dev/null &
setsid nohup "$B" 1600 0.7 65536 1 1024 8192 0 > lad_n1600_s1.csv 2> lad_n1600_s1.err < /dev/null &
sleep 1
ps aux | grep breathe | grep -v grep | awk '{print $NF, $(NF-4)}'
