#!/bin/bash
# The decisive sweep (predictions.md already written). Shipped configurations only:
# scenario::plane, Config::default, Order::Sparse, threads 1. ~4 min wall total.
set -e
T=/home/glmlab/lab-target-0/release/plane_events
mkdir -p data
echo "== A: rtf=1 m=48, seeds 1..15 x 60000 frames (16.7 min of play each)"
for s in $(seq 1 15); do $T 60000 1 $s 48 sp data/A_s$s; done
echo "== digest control at sweep scale: seed 1 flat vs item"
$T 60000 1 1 48 sp data/A_s1f flat
echo "== H: one hour of play, seed 99 (216000 frames, 3 parts)"
$T 216000 1 99 48 sp data/H_s99
echo "== B: rtf=16 m=48, seeds 1..4 x 60000 frames (4.4 h game time each)"
for s in $(seq 1 4); do $T 60000 16 $s 48 sp data/B_s$s; done
echo "== C: rtf=1 m=400 (bench clamp), seeds 1..4"
for s in $(seq 1 4); do $T 60000 1 $s 400 sp data/C_s$s; done
