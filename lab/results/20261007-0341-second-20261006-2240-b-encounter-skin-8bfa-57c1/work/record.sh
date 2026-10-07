#!/bin/sh
# Record part 1 (fast cases): the original run's case list plus this run's 64-orbit
# amortization case and the checker's ring-1e-6 combo. Raw per-case files keep the
# original run's names. Run from this directory.
T=${1:-/home/glmlab/lab-target-0/release}
: > results.jsonl
for cmd in \
  "belt 1e-4 0.3 4" \
  "belt 1e-6 0.3 4" \
  "belt 1e-8 0.3 4" \
  "belt 1e-4 0.3 16" \
  "ring 1e-4 0.3 4" \
  "fleet 1e-6 0.3 4" \
  "belt 1e-6 0.3 4 orb=64" \
  "ring 1e-6 0.3 4" \
  ; do
  echo "# $T/skin $cmd" >> results.jsonl
  $T/skin $cmd >> results.jsonl 2>&1
done
$T/skin belt 1e-4 0.3 4 > belt1e-4.out 2>&1
$T/skin belt 1e-6 0.3 4 > belt1e-6.out 2>&1
$T/skin belt 1e-8 0.3 4 > belt1e-8.out 2>&1
$T/skin ring 1e-4 0.3 4 > ring1e-4.out 2>&1
$T/skin fleet 1e-6 0.3 4 > fleet1e-6.out 2>&1
echo DONE1
