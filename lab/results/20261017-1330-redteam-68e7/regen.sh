#!/usr/bin/env bash
# Regenerates every number in dossier.md (run id 20261017-1330-redteam-68e7).
# The runner applies work/patch.diff first; this script needs only cargo + python3.
# Quiet 8-core box: ~9 min (identity suite debug ~7 min + rung release ~2 min). Under 15 min.
set -euo pipefail
cd "$(dirname "$0")/../../.."
OUT=lab/results/20261017-1330-redteam-68e7
mkdir -p "$OUT/rows"

echo "== 1. The blocker claim: does the shipped sparse-vs-dense suite run on Linux? =="
# (debug profile, as the shipped suite is run; 9 tests, each one scene)
cargo test -p emergent-engine --test identity 2>&1 | tail -3

echo "== 2. The r5 rung: harness rows (release; the integer law is profile-independent) =="
R5_OUT="$OUT/rows" cargo test --release -p emergent-engine --test r5_dense_order 2>&1 | tail -14

echo "== 3. metrics.json and the mechanical verdict =="
python3 "$OUT/metrics.py" "$OUT/rows" | tee "$OUT/metrics.json"
python3 lab/verdict.py "$OUT/r5-dense-order.md" "$OUT/metrics.json"
