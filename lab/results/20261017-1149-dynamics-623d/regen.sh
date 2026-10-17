#!/bin/sh
# Regenerates every number in dossier.md: applies the probe patch to a pristine tree,
# builds, runs the three ensembles and the composition. ~2 min on this box.
set -e
cd "$(dirname "$0")/../../.."
if ! grep -q "mod lyap;" xtask/src/main.rs; then
  git apply lab/results/20261017-1149-dynamics-623d/work/patch.diff
fi
R=lab/results/20261017-1149-dynamics-623d
LYAP_OUT=$R/work/lyap_control.jsonl   cargo run --release -p xtask -- lyap control   > $R/work/out_control.txt
LYAP_OUT=$R/work/lyap_belt.jsonl      cargo run --release -p xtask -- lyap belt      > $R/work/out_belt.txt
LYAP_OUT=$R/work/lyap_coorbital.jsonl cargo run --release -p xtask -- lyap coorbital > $R/work/out_coorbital.txt
python3 $R/analyze.py
