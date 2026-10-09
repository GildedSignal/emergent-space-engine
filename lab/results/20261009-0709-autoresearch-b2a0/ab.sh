#!/bin/sh
# Interleaved A/B: A=baseline (git stash), B=patched. 2 pairs, first line only.
cd /home/glmlab/actions-runner/_work/emergent-space-engine/lab-2
BIN=/home/glmlab/lab-target-2/release/compile-bench
MODE=${1:-tune}
for i in 1 2; do
  git stash -q
  (cd lab/results/20261009-0709-autoresearch-b2a0/bench && cargo build --release >/dev/null 2>&1)
  echo "A$i: $($BIN $MODE 0.2 2>/dev/null | head -1)"
  git stash pop -q
  (cd lab/results/20261009-0709-autoresearch-b2a0/bench && cargo build --release >/dev/null 2>&1)
  echo "B$i: $($BIN $MODE 0.2 2>/dev/null | head -1)"
done
