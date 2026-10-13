#!/usr/bin/env bash
# Regenerates every number in dossier.md from the patched tree (work/patch.diff is applied
# before this runs). ~6 minutes: two builds, four probe runs, the universe suite.
set -euo pipefail
cd "$(dirname "$0")/../../.."

run() { cargo run --release -q -p emergent-universe --example lazy_probe -- "$@"; }

echo "== quiet frames, lazy arm =="
run quiet | tee lab/results/20261012-2257-spacex-5eb6/quiet-lazy.json
echo "== quiet frames, legacy arm (ES_EAGER=1: the shipped frame loop) =="
ES_EAGER=1 run quiet | tee lab/results/20261012-2257-spacex-5eb6/quiet-legacy.json
echo "== the plane to a canonical cut, lazy arm =="
run fly | tee lab/results/20261012-2257-spacex-5eb6/fly-lazy.json
echo "== the plane to a canonical cut, legacy arm =="
ES_EAGER=1 run fly | tee lab/results/20261012-2257-spacex-5eb6/fly-legacy.json
echo "== digest comparison =="
python3 lab/results/20261012-2257-spacex-5eb6/compare.py

echo "== the universe suite (cross-schedule digest gauntlet) =="
cargo test --release -p emergent-universe 2>&1 | tail -6
