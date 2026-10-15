#!/bin/sh
# Regenerates every number in the dossier from shipped code + this run's patch (work/patch.diff,
# applied by the runner before this runs). Order: build, then the four arms. Budget: about 15 minutes
# on a quiet 8-vCPU box (B2's wall cap is 480 s, A1/A2 about 3-4 minutes each).
set -e
cd "$(dirname "$0")"
BIN=/home/glmlab/lab-target-1/release/examples/scan_cap
OUT=out
mkdir -p $OUT
# B1: the ruin, bounded for a shared box (SELF_KILL at 1.5 GB; shipped dies at the box's OOM).
ES_RSS_LIMIT_MB=1500 timeout 260 $BIN 100000 8 1 16000 100 1 > $OUT/b1-ruin-1e5.txt 2>&1 || test $? -eq 9
# B2: the same flight under the standing cap (memory flat; the 480 s wall cap ends it before the cut:
# the answer bill throttles play to ~3.6x real time, which is the finding).
ES_SCAN_STANDING=64 ES_RSS_LIMIT_MB=1500 timeout 470 $BIN 100000 8 1 16000 100 1 > $OUT/b2-cap64-1e5.txt 2>&1 || test $? -eq 8
# A1/A2: the digest-identity pair at 10^4, where both arms complete the cut.
timeout 470 $BIN 10000 8 1 16000 100 1 > $OUT/a1-off-1e4.txt 2>&1 || true
ES_SCAN_STANDING=64 timeout 470 $BIN 10000 8 1 16000 100 1 > $OUT/a2-cap64-1e4.txt 2>&1 || true
# C1/C2: inertness at Home (the cap must never fire and move nothing).
timeout 200 $BIN 100000 8 1 4000 100 0 > $OUT/c1-home-off.txt 2>&1 || true
ES_SCAN_STANDING=64 timeout 200 $BIN 100000 8 1 4000 100 0 > $OUT/c2-home-cap64.txt 2>&1 || true
echo "--- digests ---"
grep -h "cut at" $OUT/*.txt
grep -h "SELF_KILL\|WALL CAP" $OUT/*.txt || true
