#!/bin/sh
# Screen one ensemble: tail MU DU PHI PERIODS CAP for every (du, phi) of the 144-IC grid.
# Usage: screen.sh MU PERIODS CAP OUTDIR
BIN=/home/glmlab/lab-target-2/release/tail
MU=$1; PER=$2; CAP=$3; OUT=$4
mkdir -p "$OUT"
i=0
while [ $i -lt 12 ]; do
  du=$(python3 -c "print(-1.5 + $i*3.0/11)")
  j=0
  while [ $j -lt 12 ]; do
    phi=$(python3 -c "print(60.0 + $j*120.0/11)")
    echo "$BIN $MU $du $phi $PER $CAP > $OUT/ic-${i}-${j}.json 2>>$OUT/err.log"
    j=$((j+1))
  done
  i=$((i+1))
done | xargs -P "${JOBS:-8}" -I{} sh -c '{}'
cat $OUT/ic-*.json > $OUT/all.jsonl
wc -l $OUT/all.jsonl
