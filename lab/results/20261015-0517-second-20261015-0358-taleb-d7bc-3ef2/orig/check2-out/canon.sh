#!/bin/sh
BIN=/home/glmlab/lab-target-1/release/examples/scan_canon
cd "$(dirname "$0")"
timeout 300 $BIN 10000 8 1 16000 100 > c1-canon-off-seed1.txt 2>&1 & echo c1 $!
ES_SCAN_STANDING=64 timeout 300 $BIN 10000 8 1 16000 100 > c2-canon-cap64-seed1.txt 2>&1 & echo c2 $!
ES_SCAN_STANDING=4 timeout 300 $BIN 10000 8 1 16000 100 > c3-canon-cap4-seed1.txt 2>&1 & echo c3 $!
timeout 300 $BIN 10000 8 2 16000 100 > c4-canon-off-seed2.txt 2>&1 & echo c4 $!
ES_SCAN_STANDING=64 timeout 300 $BIN 10000 8 2 16000 100 > c5-canon-cap64-seed2.txt 2>&1 & echo c5 $!
wait
echo CANON-DONE
