#!/bin/sh
# The frames-mode matrix (the checker's named gold experiment for 9b46) plus controls.
# Each arm: name, timeout seconds, then the ruin args. Captures exit code + assert line.
R=${RUIN:-/home/glmlab/lab-target-5d87/release/examples/ruin}
cd "$(dirname "$0")"
mkdir -p out
arm() {
  name=$1; tmo=$1; :; tmo=$2; shift 2
  timeout "$tmo" "$R" "$@" > "out/$name.txt" 2>&1
  ec=$?
  line=$(grep -m1 "would revise its published tick" "out/$name.txt")
  [ -n "$line" ] && line="ASSERT: $line"
  fr=$(grep -m1 "^FRAMES" "out/$name.txt")
  echo "== $name exit=$ec ${line:-ok} | ${fr:-no-frames-line}"
}

# --- 864 grid: 3 seeds x 3 (rate, ahead) cells, 15 s each ---
for s in 1 2 3; do
  arm "f-864-r400-a025-s$s" 25 frames 24 8 6 12 1200 0.5 128 1 60 400 0.25 6 $s
  arm "f-864-r100-a005-s$s" 25 frames 24 8 6 12 1200 0.5 128 1 60 100 0.05 6 $s
  arm "f-864-r400-a100-s$s"  25 frames 24 8 6 12 1200 0.5 128 1 60 400 1.0 6 $s
done

# --- wave family at the checker's sizes (hz 60, rate 400, ahead 0.25) ---
arm f-14k-s1 75 frames 24 32 36 12 1500 0.5 128 1 60 400 0.25 35 1
arm f-28k-s1 115 frames 24 32 72 12 1500 0.5 128 1 60 400 0.25 50 1
arm f-28k-s7 115 frames 24 32 72 12 1500 0.5 128 1 60 400 0.25 50 7

# --- quiet 14k (the checker's own crash family) ---

# --- held-out law: Relativistic (light-cone finality on) ---
arm f-14k-rel-s1 75 rel frames 24 32 36 12 1500 0.5 128 1 60 400 0.25 35 1

# --- batch controls on the 864 scene ---
arm b-864-chunk100-s1 70 24 8 6 12 1200 0.5 128 1 100 50 1
arm b-864-single-s1  70 24 8 6 12 1200 0.5 128 1 1200 60 1
