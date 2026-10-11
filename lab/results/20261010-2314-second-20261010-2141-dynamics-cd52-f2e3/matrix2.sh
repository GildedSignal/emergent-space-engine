#!/bin/bash
export OMP_NUM_THREADS=6
cd "$(dirname "$0")"
run(){ ./belt_lyap $2 $3 0.05 $4 $5 $6 curves/r_${1}_s$6.dat | sed "s/^/$1 /"; }
echo "== controls =="
run neg 200 0 64 200 1
run pos 50 0.01 64 20 1; run pos 50 0.01 64 20 2
echo "== E1 cadence (N=200 mu=1e-4) =="
for sp in 8 32 128; do for sd in 1 2; do run cad$sp 200 0.0001 $sp 200 $sd; done; done
echo "== E2 N-scaling (mu=1e-4) =="
for nn in 50 100 200 400; do for sd in 1 2; do run n$nn $nn 0.0001 64 200 $sd; done; done
echo "== E3 mu=1e-5 =="
run m5n200 200 0.00001 64 200 1; run m5n200 200 0.00001 64 200 2
echo "== done =="
