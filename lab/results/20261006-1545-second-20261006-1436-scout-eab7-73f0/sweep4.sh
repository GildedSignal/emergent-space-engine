#!/bin/bash
set -u
B=/home/glmlab/lab-target-3/release/lawskin
R="$(cd "$(dirname "$0")" && pwd)"
run() { local d=$R/scratch/$1; mkdir -p "$d"; cd "$d"
  $B baseline "$2" "$3" "$4" "$5" "$6" "$7" "$8" "${9}" "${10}" > baseline.txt 2>&1
  $B skin "$2" "$3" "$4" "$5" "$6" "$7" "$8" "${9}" "${10}" > skin.txt 2>&1
  grep -h -E "arm=|misses=|first_" baseline.txt skin.txt | sed "s/^/[$1] /"; }
so() { local d=$R/scratch/$1; mkdir -p "$d"; cd "$d"; cp -f $R/scratch/B1/baseline-found.txt .
  $B skin "$2" "$3" "$4" "$5" "$6" "$7" "$8" "${9}" "${10}" > skin.txt 2>&1
  grep -h -E "arm=skin|misses=|first_" skin.txt | sed "s/^/[$1] /"; }
so D1 belt 120 0.1 0.01 1e-2 128 4242 0.1 2.0
so D2 belt 120 0.1 0.01 1e-2 128 4242 0.5 12.0
so D3 belt 120 0.1 0.01 1e-2 128 4242 0.5 6.0
run G2 tang 120 0.02 0.01 3e-2 64 4242 0.5 2.0
run O2 coorb 120 0.05 0.01 1e-4 64 4242 0.5 2.0
run B0 belt 120 0.1 0.01 0 64 4242 0.5 2.0
run B1b belt 120 0.1 0.01 1e-2 128 777 0.5 2.0
echo "=== done $(date +%T)"
