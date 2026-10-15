#!/bin/sh
# Regenenerates every number in dossier.md from shipped code + this run's patch
# (work/patch.diff, applied by the runner before this runs). ~3 minutes, Linux.
set -e
cd "$(dirname "$0")/../../.." || exit 1  # the repo root
cargo build --release -p emergent-universe --example promote
BIN=$(cargo build --release -p emergent-universe --example promote 2>/dev/null; echo target/release/examples/promote)
[ -x "$BIN" ] || BIN=/home/glmlab/lab-target-2/release/examples/promote
mkdir -p lab/results/20261015-0250-scout-760f/out
for arm in "100000 coast 8 6000" "10000 coast 8 6000" "10000 burn 8 6000"; do
  "$BIN" $arm
done > lab/results/20261015-0250-scout-760f/out/runs.txt 2>&1
cat lab/results/20261015-0250-scout-760f/out/runs.txt
