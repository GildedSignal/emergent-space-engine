#!/bin/bash
# Block B-heavy: N=800 dt-axis at mu=1e-5, T=25 (see predictions.md P8 for the horizon license)
export OMP_NUM_THREADS=6
cd "$(dirname "$0")"
for sp in 64 256 1024; do for sd in 1 2 3; do
  ./belt2 800 0.00001 0.05 $sp 25 $sd curves/r2_n800_s${sp}_${sd}.dat --conj | sed "s/^/n800_s${sp} /"
done; done
echo "== B-heavy done =="
