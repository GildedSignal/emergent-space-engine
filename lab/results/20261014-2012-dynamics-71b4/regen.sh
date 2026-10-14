#!/usr/bin/env bash
# Regenerates every number in dossier.md. ~9 minutes single-core, <300 MB.
set -e
cd "$(dirname "$0")"
mkdir -p runs

echo "=== machine 2 (bounded midpoint kernel) — decisive batch, 32 bodies, H=400 ==="
for K in 8 16 32; do
  [ -f runs/A_K$K.npz ] || python3 harness2.py runs/A_K$K.npz A $K 400 128 32
done
for th in 0.1 0.5; do
  [ -f runs/C_th$th.npz ] || python3 harness2.py runs/C_th$th.npz C $th 400 128 32
done
for q in 0.0001 0.0005; do
  [ -f runs/Q_q$q.npz ] || python3 harness2.py runs/Q_q$q.npz Q $q 400 128 32
done
[ -f runs/Q_q0.0005_ws512.npz ] || python3 harness2.py runs/Q_q0.0005_ws512.npz Q 0.0005 400 512 32
[ -f runs/C_th0.5_ws512.npz ]  || python3 harness2.py runs/C_th0.5_ws512.npz  C 0.5    400 512 32

echo "=== snap diagnostic (fires snapped to the sensor grid: QUANT_SNAP=1) ==="
[ -f runs/Q_ws128_H400.npz ]  || QUANT_SNAP=1 python3 harness2.py runs/Q_ws128_H400.npz  Q 0.0005 400 128 8
[ -f runs/Q_ws512_H100.npz ]  || QUANT_SNAP=1 python3 harness2.py runs/Q_ws512_H100.npz  Q 0.0005 100 512 8
[ -f runs/Q_ws512_H400.npz ]  || QUANT_SNAP=1 python3 harness2.py runs/Q_ws512_H400.npz  Q 0.0005 400 512 8
[ -f runs/Q_ws1024_H100.npz ] || QUANT_SNAP=1 python3 harness2.py runs/Q_ws1024_H100.npz Q 0.0005 100 1024 8

echo "=== interpolated-fire emergence with horizon (8 bodies) ==="
[ -f runs/Q_ws512i_H100.npz ] || python3 harness2.py runs/Q_ws512i_H100.npz Q 0.0005 100 512 8

echo "=== machine 1 (524e's held-at-close kernel): everything compounds ==="
[ -f runs/held_A8.npz ]   || python3 harness.py runs/held_A8.npz   A 8     100 64 32
[ -f runs/held_Q1e3.npz ] || python3 harness.py runs/held_Q1e3.npz Q 0.001 100 64 32

echo "=== clock convergence order ==="
for K in 4 8 16 32; do
  [ -f runs/conv_A$K.npz ] || python3 harness2.py runs/conv_A$K.npz A $K 100 128 8
done

python3 agg.py
