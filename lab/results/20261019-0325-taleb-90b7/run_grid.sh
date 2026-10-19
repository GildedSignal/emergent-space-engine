#!/bin/bash
# Decisive grid for the formation burst law. ~27 flights, each a separate process.
set -u
BIN=${BIN:-/home/glmlab/lab-target-2/release/examples/fleetburst}
cd "$(dirname "$0")"
mkdir -p work
for n in 400 1600 6400; do
  case $n in 400) H=2048;; 1600) H=4096;; 6400) H=8192;; esac
  # aligned control (seed-free by construction)
  $BIN --scene head --n $n --aligned --horizon $H --out work/head_n${n}_sig0_aligned_s1.tsv 2>/dev/null
  # dispersion ladder
  for sig in 4096 16384 65536; do
    for s in 1 2; do
      $BIN --scene head --n $n --sigma $sig --horizon $H --seed $s --out work/head_n${n}_sig${sig}_s${s}.tsv 2>/dev/null &
    done
  done
  # thermal controls at matched box, fill, speed scale
  for s in 1 2; do
    $BIN --scene thermal --n $n --horizon $H --seed $s --out work/thermal_n${n}_s${s}.tsv 2>/dev/null &
  done
  wait
done
# seed-freeness check of the aligned control
$BIN --scene head --n 400 --aligned --horizon 2048 --seed 2 --out work/head_n400_sig0_aligned_s2.tsv 2>/dev/null
echo GRID_DONE
