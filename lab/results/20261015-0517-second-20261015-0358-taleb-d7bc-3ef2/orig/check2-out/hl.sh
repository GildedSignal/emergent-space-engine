#!/bin/sh
# Horizon-limited canonical (frame_to horizon = cut tick): the first checker's protocol, tested blind.
BIN=/home/glmlab/lab-target-1/release/examples/scan_canon2
cd "$(dirname "$0")"
timeout 300 $BIN 10000 8 2 16000 100 > h1-hl-off-seed2.txt 2>&1 & echo h1 $!
timeout 300 $BIN 10000 8 2 16000 100 > h2-hl-off-seed2-again.txt 2>&1 & echo h2 $!
ES_SCAN_STANDING=64 timeout 300 $BIN 10000 8 2 16000 100 > h3-hl-cap64-seed2.txt 2>&1 & echo h3 $!
ES_SCAN_STANDING=64 timeout 300 $BIN 10000 8 2 16000 100 > h4-hl-cap64-seed2-again.txt 2>&1 & echo h4 $!
timeout 300 $BIN 10000 8 1 16000 100 > h5-hl-off-seed1.txt 2>&1 & echo h5 $!
ES_SCAN_STANDING=4 timeout 300 $BIN 10000 8 1 16000 100 > h6-hl-cap4-seed1.txt 2>&1 & echo h6 $!
wait
echo HL-DONE
