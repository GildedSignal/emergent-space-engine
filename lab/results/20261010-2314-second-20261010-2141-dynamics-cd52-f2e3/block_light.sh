#!/bin/bash
# Light blocks: B (N=50,200), C (horizon), D (mu-axis), A (record completion)
export OMP_NUM_THREADS=6
cd "$(dirname "$0")"
echo "== B N=50/200 mu=1e-5 T=50 =="
for nn in 50 200; do for sp in 64 256 1024; do for sd in 1 2 3; do
  ./belt2 $nn 0.00001 0.05 $sp 50 $sd curves/r2_n${nn}_s${sp}_${sd}.dat --conj | sed "s/^/n${nn}_s${sp} /"
done; done; done
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
