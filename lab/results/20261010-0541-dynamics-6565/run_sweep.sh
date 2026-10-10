#!/bin/sh
# Exact reproduction of all runs (each well under 60 s except where noted).
set -e
gcc -O2 -o sim sim.c -lm
# exploratory / controls
./sim 4000 30 30 0.085 0.01 200 1 400000 smoke        # elastic default eps=1? NO: this used default 0.7; elastic runaway used the pre-restitution binary; rerun below
./sim 2000 30 30 0.12 0.01 150 11 300000 e1 0.7      # cold start, tau=0.1
./sim 2000 30 30 0.0268 0.01 150 12 300000 e2 0.7    # cold sparse
./sim 2000 30 30 0.12 0.01 200 1 400000 e_elastic 1.0  # ELASTIC RUNAWAY (~130 s)
# sweep batch 1 (warm starts, eps=0.7, N=2000, box 30x30)
./sim 2000 30 30 0.0268 0.3 150 21 400000 t0005_s21 0.7 &
./sim 2000 30 30 0.0268 0.3 150 22 400000 t0005_s22 0.7 &
./sim 2000 30 30 0.0536 0.3 150 21 400000 t002_s21 0.7 &
./sim 2000 30 30 0.0536 0.3 150 22 400000 t002_s22 0.7 &
./sim 2000 30 30 0.12 0.3 150 21 400000 t01_s21 0.7 &
./sim 2000 30 30 0.12 0.3 150 22 400000 t01_s22 0.7 &
wait
# batch 2: attractor pair + first high-tau attempts (cap-bound, superseded by batch 3)
./sim 2000 30 30 0.12 1.0 150 21 400000 t01_hot_s21 0.7 &
./sim 2000 30 30 0.12 0.01 150 21 400000 t01_cold_s21 0.7 &
wait
# batch 3: steady windows at high tau (N=1000; tau fixed via R)
./sim 1000 15 15 0.1342 0.3 100 21 600000 t20n_s21 0.7 &
./sim 1000 15 15 0.1342 0.3 100 22 600000 t20n_s22 0.7 &
./sim 1000 30 30 0.3795 0.3 100 21 600000 t05n_s21 0.7 &
wait
for f in *.events.bin; do gzip -f "$f"; done
python3 post.py
