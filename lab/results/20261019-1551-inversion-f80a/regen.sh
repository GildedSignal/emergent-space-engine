#!/bin/sh
# Regen (from a clean checkout): apply this run's patch, build, re-fly both arms,
# print the window table. ~11 min on the lab box (two flights: 175 s + 420 s wall).
# Patch = e181's work/patch.diff verbatim + frame-loop prune() RESTORED (its checker's
# correction (a)) + history_census probe. TTL unset == shipped behaviour again.
set -e
cd "$(dirname "$0")/../../.." # repo root
git apply lab/results/20261019-1551-inversion-f80a/work/patch.diff || echo "patch already applied"
cargo build --release -p emergent-universe --example nladder
sh lab/results/20261019-1551-inversion-f80a/work/run_flights.sh
python3 lab/results/20261019-1551-inversion-f80a/analyze.py
