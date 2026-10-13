#!/bin/sh
# Regen: every number in dossier.md, from shipped code + work/patch.diff.
# Total wall on the 8-vCPU runner: ~4 min (two release builds dominate).
set -e
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"   # repo root
RUN="$(dirname "$0")"

cd "$ROOT"
git apply "$RUN/work/patch.diff" 2>/dev/null || git apply --reverse --check "$RUN/work/patch.diff" || { echo "patch does not apply"; exit 1; }

echo "=== A. division primitives: fuzz (10^7) + timing (Tables 1-2 of the dossier) ==="
cd "$RUN/bench"
cargo run --release 2>/dev/null

echo ""
echo "=== B. the compile workload: census, repetition, bit-identity, arms (Table 3) ==="
cd "$ROOT"
cargo run --release -p emergent-space --example compile_bench 2>/dev/null

echo ""
echo "=== C. per-node ingredients: isqrt / cos / mul controls (Table 4) ==="
cargo run --release -p emergent-space --example ingredient_bench 2>/dev/null
