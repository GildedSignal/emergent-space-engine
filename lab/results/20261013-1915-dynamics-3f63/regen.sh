#!/usr/bin/env bash
# Regenerate every number in dossier.md (run 20261013-1915-dynamics-3f63) from the shipped tree.
# Applies work/patch.diff first if the probe is absent (the tree is restored after each run).
set -euo pipefail
cd "$(dirname "$0")/../../.."   # the repo root

if [ ! -f crates/universe/tests/crash_basin.rs ] && [ -f lab/results/20261013-1915-dynamics-3f63/work/patch.diff ]; then
  git apply lab/results/20261013-1915-dynamics-3f63/work/patch.diff
fi

R="cargo test --release -p emergent-universe --test crash_basin -- --nocapture"

echo '== pilot (validation against the page D row) =='
BASIN_MODE=pilot $R 2>&1 | grep -E 'fly '

echo '== coast control =='
BASIN_MODE=coast $R 2>&1 | grep -E 'coast:'

echo '== anchors: 16 levels at 1.099R =='
BASIN_MODE=anchors $R 2>&1 | grep -E 'fly '

echo '== sweep: r-bisection at levels 0-6 =='
BASIN_MODE=sweep BASIN_LEVELS=0,1,2,3,4,5,6 $R 2>&1 | grep -E 'r\*'

echo '== held-out arms (plus the determinism repeat) =='
BASIN_MODE=heldout BASIN_ARMS='2.30L0;2.50L0;1.55L2;1.70L2;2.30L0' $R 2>&1 | grep -E 'fly '

echo '== analysis: every derived number in the dossier =='
python3 lab/results/20261013-1915-dynamics-3f63/analysis.py
