#!/usr/bin/env bash
# Regenerates every number in dossier.md for run 20261015-0724-dynamics-1648.
# The runner applies work/patch.diff (the skipgas example + its dev-dependency) before
# this runs. Budget: ~10 min on the lab box (single-threaded example, 5 scenes x 5 arms).
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
cargo run --release -p emergent-lattice --example skipgas \
  > lab/results/20261015-0724-dynamics-1648/work/results.jsonl \
  2> lab/results/20261015-0724-dynamics-1648/work/run.err
python3 lab/results/20261015-0724-dynamics-1648/analyze.py \
  lab/results/20261015-0724-dynamics-1648/work/results.jsonl \
  | tee lab/results/20261015-0724-dynamics-1648/work/analysis.txt
