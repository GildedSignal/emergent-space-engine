#!/bin/sh
# Regenenerates every number in dossier.md from the shipped code plus this run's patch
# (work/patch.diff, applied by the runner before this runs). Total wall < 2 min.
cd "$(dirname "$0")/../../.."   # repo root (lab/results/<run> is three deep)
cargo run --release -p emergent-space --example elliptic_probe \
  > "$(dirname "$0")/probe-out.txt" 2>&1
echo "wrote probe-out.txt ($(wc -l < "$(dirname "$0")/probe-out.txt") lines)"
