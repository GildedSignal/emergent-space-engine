#!/bin/bash
# Regen for run 20261020-1621-system-7fd3 (whole-system lens): the mint census.
# Rebuilds the shipped tree + this run's print-only patch (work/patch.diff), runs the two
# decisive belt arms with ES_MINT_CENSUS=1, and reprints every dossier number from the logs.
set -e
cd "$(dirname "$0")/../../.."   # the repo root
git apply --check lab/results/20261020-1621-system-7fd3/work/patch.diff 2>/dev/null || true
git apply lab/results/20261020-1621-system-7fd3/work/patch.diff 2>/dev/null || echo "patch already applied"
cargo build --release -p emergent-universe --example nladder --target-dir /home/glmlab/lab-target-3
mkdir -p lab/results/20261020-1621-system-7fd3/out
for arm in "10000" "30000"; do
  ES_MINT_CENSUS=1 /home/glmlab/lab-target-3/release/examples/nladder "$arm" coast 60 1800 \
    > "lab/results/20261020-1621-system-7fd3/out/arm-${arm}.log" 2>&1
done
python3 lab/results/20261020-1621-system-7fd3/compose.py
