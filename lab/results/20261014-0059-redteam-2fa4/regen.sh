#!/bin/sh
# Regenerates every number in dossier.md from shipped code + this run's patch
# (work/patch.diff, applied by the runner before this runs). < 1 minute.
set -e
cd "$(dirname "$0")/../../.."   # repo root
echo "== building the oracle example =="
cargo build --release -p emergent-universe --example seen_oracle 2>&1 | tail -1
echo "== the seen instruments vs the SR oracle (dossier: exact-path + Δte note) =="
cargo run --release -p emergent-universe --example seen_oracle -- 6 \
  | tee lab/results/20261014-0059-redteam-2fa4/oracle.txt
echo "== the three seams (dossier: S1/S2/S3 tables) =="
cd lab/results/20261014-0059-redteam-2fa4 && python3 seams.py | tee seams.txt
