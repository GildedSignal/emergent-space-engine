#!/bin/bash
cd "$(dirname "$0")"
B=/home/glmlab/lab-target-1/release/examples/race
: > exits.txt
run() { local tag=$1; shift; timeout 90 "$B" "$@" > "$tag.out" 2> "$tag.err" && echo "$tag exit=0" >> exits.txt || echo "$tag exit=$?" >> exits.txt; }
run a1_nosab 400 11 1 900 2 16 8 128 60 x 0.3 &
run a2_win32 3000 11 1 2400 4 32 8 64 40 3 1.0 &
run a3_seed33 3000 33 1 2400 4 16 8 64 40 3 1.0 &
run a4_sab6 3000 11 1 4800 6 16 8 64 40 6 2.0 &
run a5_v320 1000 33 1 600 6 16 8 320 200 3 1.0 &
run a6_long 3000 101 1 2400 8 16 8 64 40 3 1.0 &
wait
cat exits.txt
