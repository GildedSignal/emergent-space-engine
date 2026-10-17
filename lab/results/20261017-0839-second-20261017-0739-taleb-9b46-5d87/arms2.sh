#!/bin/sh
# Exposure-matched completions of the frames matrix: the quiet arm must reach the tick
# range where the checker's quiet BATCH crash fired (chunk 2, ticks 150-300), and the
# relativistic arm (light-cone finality: fin_hi may exceed the frontier) needs real
# conflict exposure. Plus the quiet batch twin on this box.
R=${RUIN:-/home/glmlab/lab-target-5d87/release/examples/ruin}
cd "$(dirname "$0")"
mkdir -p out
arm() {
  name=$1; tmo=$2; shift 2
  timeout "$tmo" "$R" "$@" > "out/$name.txt" 2>&1
  ec=$?
  line=$(grep -m1 "would revise its published tick" "out/$name.txt")
  [ -n "$line" ] && line="ASSERT: $line"
  fr=$(grep -m1 -E "^FRAMES|^DONE|^DNF" "out/$name.txt")
  echo "== $name exit=$ec ${line:-ok} | ${fr:-none}"
}

# quiet 14k frames, deep: 420 s should carry the frontier past 300 (0.75 chr/s measured)
arm f-q14k-deep-s1 440 frames 24 32 36 12 1500 0.5 1 1 60 400 0.25 300 1

# relativistic, real exposure: 864 (3 cadences/seeds) and a deeper 14k
arm f-864-rel-r400-a025-s1 70 rel frames 24 8 6 12 1200 0.5 128 1 60 400 0.25 20 1
arm f-864-rel-r100-a005-s2 70 rel frames 24 8 6 12 1200 0.5 128 1 60 100 0.05 20 2
arm f-864-rel-r400-a100-s1 70 rel frames 24 8 6 12 1200 0.5 128 1 60 400 1.0 20 1
arm f-14k-rel-deep-s1 200 rel frames 24 32 36 12 1500 0.5 128 1 60 400 0.25 45 1

# the quiet batch twin on this box (the checker's crash arm: chunk 150)
arm b-q14k-chunk150-s1 260 24 32 36 12 1500 0.5 1 1 150 250 1

# --- chunk-grid mechanism probes (the window-grid rule: on-grid targets never crash) ---
for ch in 96 112 128 100 104 108; do
  arm "b-864-chunk$ch-s1" 90 24 8 6 12 1200 0.5 128 1 $ch 80 1
done
arm b-864-chunk100-s2 90 24 8 6 12 1200 0.5 128 1 100 80 2
arm b-14k-chunk512-s1 120 24 32 36 12 1500 0.5 128 1 512 110 1
arm b-14k-chunk504-s1 120 24 32 36 12 1500 0.5 128 1 504 110 1
