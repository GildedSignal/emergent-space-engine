#!/bin/sh
# Reproduce every number in dossier.md. Linux/x86 (agonbox-class), each step < 60 s.
set -e
cd "$(dirname "$0")"
TARGET=${TARGET:-/home/glmlab/lab-target-2/release/examples}   # cargo build --release -p emergent-shipmem --example measure --example ladder
mkdir -p data
for args in "traders 1e6 100000" "stream 1e6 100000" "convoy 1e6 100000" "battle 2e5 100000" "random 1e6 0"; do
  $TARGET/measure $args 128 data/measure.jsonl
done
for r in 0 1e-4 1e-3 1e-2 1e-1 0.3 1 poisson random; do
  $TARGET/ladder $r 4096 64 10000 data/ladder.jsonl
done
python3 budget.py
