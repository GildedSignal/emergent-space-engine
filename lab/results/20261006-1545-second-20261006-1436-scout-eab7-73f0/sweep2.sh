#!/bin/bash
# Second-author sweep: the law's own kick stream (32 kicks/orbit) through the scout run's arms.
set -u
B=/home/glmlab/lab-target-3/release/lawskin
R="$(cd "$(dirname "$0")" && pwd)"

run() { # dir scene n sigma_e rho rg epochs seed slack widen
  local d=$R/scratch/$1; mkdir -p "$d"; cd "$d"
  echo "=== $1: baseline $(date +%T)"
  $B baseline "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9" "${10}" > baseline.txt 2>&1
  echo "=== $1: skin $(date +%T)"
  $B skin "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9" "${10}" > skin.txt 2>&1
  grep -h -E "arm=|per_epoch|misses" baseline.txt skin.txt | sed "s/^/[$1] /"
}

#        case   scene  n   sige  rho  rg     ep   seed  slack widen
run B2   belt   120 0.1  0.01 3e-3   128  4242  0.5   2.0
run B3   belt   120 0.1  0.01 3e-2   64   4242  0.5   2.0
run B4   belt   120 0.1  0.01 1e-4   64   4242  0.5   2.0
run G1   tang   120 0.02 0.01 1e-2   128  4242  0.5   2.0
run G1b  tang   120 0.02 0.01 1e-2   128  777   0.5   2.0
run G2   tang   120 0.02 0.01 3e-2   64   4242  0.5   2.0
run O1   coorb  120 0.05 0.01 1e-2   64   4242  0.5   2.0
run O2   coorb  120 0.05 0.01 1e-4   64   4242  0.5   2.0
# negative control: stale windows (widen 0) under systematic drift, own 64-epoch truth
run N1   belt   120 0.1  0.01 1e-2   64   4242  0.5   0
echo "=== done $(date +%T)"
