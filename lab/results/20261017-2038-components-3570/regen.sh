#!/usr/bin/env bash
# Regen: applies work/patch.diff, builds, reflies the decisive arm, re-runs the census.
# Total wall ~5-8 min on the lab's 8 vCPU box (build dominates if cold).
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261017-2038-components-3570

git apply --check "$R/work/patch.diff" 2>/dev/null && git apply "$R/work/patch.diff" || echo "patch already applied or tree dirty; continuing"
cargo build --release -p emergent-universe --example nladder

EXE="${CARGO_TARGET_DIR:-target}/release/examples/nladder"
BOUND_PROBE=1 "$EXE" 10000 coast 150 1800 >"$R/work/regen.out" 2>"$R/work/regen.err"
python3 "$R/analyze.py" "$R/work/regen.err" | tee "$R/work/census-regen.json"
echo "--- author's census (for comparison) ---"
cat "$R/work/census.json"
