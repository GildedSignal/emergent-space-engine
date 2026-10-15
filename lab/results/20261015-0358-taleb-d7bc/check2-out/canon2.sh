#!/bin/sh
# Disambiguate the seed-2 canonical split: is it the cap or lookahead residue?
BIN=/home/glmlab/lab-target-1/release/examples/scan_canon
cd "$(dirname "$0")"
# rerun at margin 120 (stability of the split)
timeout 300 $BIN 10000 8 2 16000 100 > c6-canon-off-seed2-m120.txt 2>&1 & echo c6 $!
ES_SCAN_STANDING=64 timeout 300 $BIN 10000 8 2 16000 100 > c7-canon-cap64-seed2-m120.txt 2>&1 & echo c7 $!
# margin 600 (stop 10 game-s early; less lookahead overshoot)
ES_CANON_MARGIN=600 timeout 300 $BIN 10000 8 2 16000 100 > c8-canon-off-seed2-m600.txt 2>&1 & echo c8 $!
ES_SCAN_STANDING=64 ES_CANON_MARGIN=600 timeout 300 $BIN 10000 8 2 16000 100 > c9-canon-cap64-seed2-m600.txt 2>&1 & echo c9 $!
# seed 1 control at margin 600
ES_CANON_MARGIN=600 timeout 300 $BIN 10000 8 1 16000 100 > c10-canon-off-seed1-m600.txt 2>&1 & echo c10 $!
ES_SCAN_STANDING=4 ES_CANON_MARGIN=600 timeout 300 $BIN 10000 8 1 16000 100 > c11-canon-cap4-seed1-m600.txt 2>&1 & echo c11 $!
wait
echo CANON2-DONE
