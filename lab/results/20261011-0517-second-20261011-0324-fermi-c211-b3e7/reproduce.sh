#!/bin/sh
# Reproduce every number in dossier.md. Linux/x86, each step < 60 s.
# Baseline (the original run's own script, shipped code) + the kick-magnitude rung + budget.
set -e
cd "$(dirname "$0")"
TARGET=${TARGET:-/home/glmlab/lab-target-0/release/examples}  # cargo build --release -p emergent-shipmem --example measure --example ladder
mkdir -p data

# 1. The original run's record, from shipped code only (bit-identical constants).
for args in "traders 1e6 100000" "stream 1e6 100000" "convoy 1e6 100000" "battle 2e5 100000" "random 1e6 0"; do
  $TARGET/measure $args 128 data/measure.jsonl
done
for r in 0 1e-4 1e-3 1e-2 1e-1 0.3 1 poisson random; do
  $TARGET/ladder $r 4096 64 10000 data/ladder.jsonl
done

# 2. The kick-magnitude rung (this run's experiment; standalone crate, no crate edits).
(cd kickmag && CARGO_TARGET_DIR=$PWD/target cargo build --release --bins)
sh sweep.sh

# 3. The budget, with the magnitude-dependent admission rule and the restated headline.
python3 budget.py
