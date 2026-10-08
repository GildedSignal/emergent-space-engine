#!/bin/sh
# Reproduces every number in dossier.md. Each step < 60 s unless noted. ~40 s total.
# Linux/x86 cloud runner, 8 vCPU shared, timings are order-of-magnitude only.
set -e
cd "$(dirname "$0")"
export CARGO_TARGET_DIR=/tmp/crossing-target
cargo build --release 2>&1 | tail -1
B=$CARGO_TARGET_DIR/release/crossing
echo "--- control: zero-miss vs truth (m=100 per lane)"
$B verify 100
echo "--- within-lane blocks (the gold's regime)"
for m in 125 250 500; do $B block $m aa; $B block $m bb; done
echo "--- crossing block ladder"
for m in 125 250 500 1000 2000; do $B block $m ab; done
echo "--- candidate generation (no pruning possible)"
for m in 500 1000 2000; do $B cone $m; done
echo "--- corridor invariant"
$B cluster 500
$B cluster 1000
echo "--- diffuse-belt control (shipped binary, same rho, same horizon)"
cd ../../../../../ && CARGO_TARGET_DIR=/tmp/crossing-target cargo build --release -p emergent-encounters 2>&1 | tail -1
/tmp/crossing-target/release/encounters steady 2000 1e-3 20
