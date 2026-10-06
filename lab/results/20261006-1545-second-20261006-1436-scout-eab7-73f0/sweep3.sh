#!/bin/bash
set -u
B=/home/glmlab/lab-target-3/release/lawskin
R="$(cd "$(dirname "$0")" && pwd)"
run() { local d=$R/scratch/$1; mkdir -p "$d"; cd "$d"
  $B baseline "$2" "$3" "$4" "$5" "$6" "$7" "$8" "${9}" "${10}" > baseline.txt 2>&1
  $B skin "$2" "$3" "$4" "$5" "$6" "$7" "$8" "${9}" "${10}" > skin.txt 2>&1
  grep -h -E "arm=|misses=|first_" baseline.txt skin.txt | sed "s/^/[$1] /"; }
skinonly() { local d=$R/scratch/$1; mkdir -p "$d"; cd "$d"
  $B skin "$2" "$3" "$4" "$5" "$6" "$7" "$8" "${9}" "${10}" > skin.txt 2>&1
  grep -h -E "arm=|misses=|first_" skin.txt | sed "s/^/[$1] /"; }
run   N1  belt  120 0.1  0.01 1e-2 64  4242 0.5 0
run   O1  coorb 120 0.05 0.01 1e-2 64  4242 0.5 2.0
run   G1b tang  120 0.02 0.01 1e-2 128 777  0.5 2.0
# regenerate B1 truth (for the record and the fix-attribution arms)
run   B1  belt  120 0.1  0.01 1e-2 128 4242 0.5 2.0
# fix attribution vs B1's truth: tighter slack / geometry-scaled widening
cp -r $R/scratch/B1 $R/scratch/D0; rm $R/scratch/D0/skin.txt
skinonly D1 belt 120 0.1 0.01 1e-2 128 4242 0.1 2.0
cp $R/scratch/B1/baseline-found.txt $R/scratch/D1/
skinonly D2 belt 120 0.1 0.01 1e-2 128 4242 0.5 12.0
cp $R/scratch/B1/baseline-found.txt $R/scratch/D2/
echo "=== done $(date +%T)"
