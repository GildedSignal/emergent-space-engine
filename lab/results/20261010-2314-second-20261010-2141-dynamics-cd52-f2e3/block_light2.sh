#!/bin/bash
# Light blocks, remainder after the 300s kill: n200_s1024 seeds 2-3, C, D, A
export OMP_NUM_THREADS=4
cd "$(dirname "$0")"
for sd in 2 3; do
  ./belt2 200 0.00001 0.05 1024 50 $sd curves/r2_n200_s1024_${sd}.dat --conj | sed "s/^/n200_s1024 /"
done
echo "== C horizon N=200 T=25 =="
for sp in 64 1024; do for sd in 1 2 3; do
  ./belt2 200 0.00001 0.05 $sp 25 $sd curves/r2_h${sp}_${sd}.dat --conj | sed "s/^/h${sp} /"
done; done
echo "== D mu-axis N=200 T=50 =="
for mu in 0.000001 0.0000001; do for sp in 64 1024; do for sd in 1 2 3; do
  ./belt2 200 $mu 0.05 $sp 50 $sd curves/r2_m${mu}_s${sp}_${sd}.dat --conj | sed "s/^/m${mu}_s${sp} /"
done; done; done
echo "== A record completion mu=1e-4 T=200 (corrected cad64/cad256 for E1) =="
for sp in 64 256; do for sd in 1 2; do
  ./belt2 200 0.0001 0.05 $sp 200 $sd curves/r2_cad${sp}_s${sd}.dat --conj | sed "s/^/cad${sp} /"
done; done
echo "== light done =="
