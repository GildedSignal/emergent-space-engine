#!/bin/bash
# Heavy remainder: N=800 spon=1024 (seeds 1-3), T=25, mu=1e-5
export OMP_NUM_THREADS=4
cd "$(dirname "$0")"
for sd in 1 2 3; do
  ./belt2 800 0.00001 0.05 1024 25 $sd curves/r2_n800_s1024_${sd}.dat --conj | sed "s/^/n800_s1024 /"
done
echo "== B-heavy done =="
