#!/bin/bash
# Decisive matrix (predictions.md already written).
export OMP_NUM_THREADS=6
cd "$(dirname "$0")"
run(){ ./belt_lyap $2 $3 0.05 $4 $5 $6 curves/${1}_s$6.dat | sed "s/^/$1 /"; }
echo "== controls =="
run pos 50 0.01 64 20 1; run pos 50 0.01 64 20 2
run neg 200 0 64 200 1; run neg 200 0 64 200 2; run neg 200 0 64 200 3
echo "== E1 cadence (N=200 mu=1e-4) =="
for sp in 4 8 16 32 64 256; do for sd in 1 2 3; do run cad$sp 200 0.0001 $sp 200 $sd; done; done
echo "== E2 N-scaling (mu=1e-4) =="
for nn in 50 100 200 400 800; do for sd in 1 2 3; do run n$nn $nn 0.0001 64 200 $sd; done; done
echo "== E3 mu=1e-5 (law check + scaling) =="
for nn in 200 800; do for sd in 1 2 3; do run m5n$nn $nn 0.00001 64 200 $sd; done; done
echo "== done =="
