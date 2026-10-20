#!/bin/bash
# Regen for run 20261020-1729-second-20261020-1621-system-7fd3-aa42 (second author on 7fd3):
# the compile-share adjudication. Rebuilds the shipped tree + work/patch.diff (7fd3's census
# verbatim + two stage timers inside from_state + census printing in the kick-bench), then runs
# a765's bench arm (seeds 1/7/42 + a seed-1 repeat) and 7fd3's belt arm, and reprints every
# dossier number via compose.py.  Wall ~4 min.
#
# NOTE (b583's lesson, honoured here): build xtask and the nladder example in SEPARATE cargo
# invocations — a single `cargo build -p xtask -p emergent-universe --example nladder` never
# builds xtask (the --example filter selects example targets in every package).
set -e
cd "$(dirname "$0")/../../.."   # the repo root
R=lab/results/20261020-1729-second-20261020-1621-system-7fd3-aa42
T=/home/glmlab/lab-target-aa42

git apply --check "$R/work/patch.diff" 2>/dev/null && git apply "$R/work/patch.diff" || echo "patch already applied"

cargo build --release -p xtask --target-dir "$T" -j4
cargo build --release -p emergent-universe --example nladder --target-dir "$T" -j4
X="$T/release/xtask"; N="$T/release/examples/nladder"
strings "$X" | grep -q "ucensus\[universe\]" || { echo "xtask stale (no census strings)"; exit 1; }
strings "$N" | grep -q "fit_ms" || { echo "nladder stale (no stage timers)"; exit 1; }

mkdir -p "$R/out"; cat /proc/loadavg > "$R/out/loadavg-at-runs.txt"
for s in 1 42 7; do
  ES_MINT_CENSUS=1 "$X" universe --kick-bench --seed "$s" --rtf 100 --seconds 10 > "$R/out/bench-s$s.log" 2>&1
done
ES_MINT_CENSUS=1 "$X" universe --kick-bench --seed 1 --rtf 100 --seconds 10 > "$R/out/bench-s1b.log" 2>&1
for arm in 10000 30000; do
  ES_MINT_CENSUS=1 "$N" "$arm" coast 60 1800 > "$R/out/belt-${arm}.log" 2>&1
done
python3 "$R/compose.py"
