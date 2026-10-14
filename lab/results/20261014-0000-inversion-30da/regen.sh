#!/bin/sh
# Regenerates every number in dossier.md (20261014-0000-inversion-30da).
# work/patch.diff (the flight_growth test) must be applied before this runs.
# Budget: ~10 min (build ~1 min, table ~20 s, corpus ~4 min, baselines ~1 min).
set -e
cd "$(dirname "$0")/../../.."   # repo root

mkdir -p lab/results/20261014-0000-inversion-30da/work

echo '== build (with the patch) =='
cargo build --release -p xtask 2>&1 | tail -1

echo '== baseline: the committed corpus today (evidence 2) =='
time cargo run --release -q -p xtask -- universe --replay-all 2>&1 | tail -2

echo '== per-flight replay of the committed flights (evidence 3) =='
for f in artifacts/flights/*.json; do
  cargo run --release -q -p xtask -- universe --replay "$f" --seconds 30 2>/dev/null | grep -E '^  [0-9]+ inputs|^match'
done

echo '== growth table + corpus demonstration (evidence 4, 5) =='
cargo test --release -p xtask --bin xtask the_gate_ -- --nocapture --test-threads=1 2>&1 \
  | tee lab/results/20261014-0000-inversion-30da/work/tests.log \
  | grep -E 'GROWTH|CORPUS|GATE exit|skipped|test result'
