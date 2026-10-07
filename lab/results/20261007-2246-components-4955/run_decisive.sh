#!/usr/bin/env bash
# Decisive grid for run 20261007-2246-components-4955. Each cell ≤ ~60 s.
set -u
cd "$(dirname "$0")"
BIN=$CARGO_TARGET_DIR/release/qbench
OUT=metrics.jsonl
: > "$OUT"
state() { { echo "== $(date -u +%FT%TZ)"; cat /proc/loadavg; grep MemAvailable /proc/meminfo; } >> machine-state.log; }
state
PIN=""
command -v taskset >/dev/null && PIN="taskset -c 3"
for seed in 1 2 3; do
  # belt: the law's default cadence, 32 kicks/orbit, ~325x period span
  $PIN $BIN belt 100000 2000000 $seed time >> "$OUT" || exit 2
  $PIN $BIN belt 1000000 4000000 $seed time >> "$OUT" || exit 2
  # formation: co-orbital fleet, same-tick batches
  $PIN $BIN formation 1000000 3000000 $seed time >> "$OUT" || exit 2
  # averaged: ~1 kick/orbit (H0190), huge lookahead
  $PIN $BIN averaged 1000000 4000000 $seed time >> "$OUT" || exit 2
  # perturbed: handoff-like cancels + earlier re-sets
  $PIN $BIN perturbed 1000000 4000000 $seed time >> "$OUT" || exit 2
done
# scaling top rung (single seed, largest memory cell)
$PIN $BIN belt 10000000 10000000 1 time >> "$OUT" || exit 2
state
echo done
