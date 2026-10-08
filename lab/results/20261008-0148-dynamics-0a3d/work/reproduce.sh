#!/usr/bin/env bash
# Reproduce lab/results/20261008-0148-dynamics-0a3d (exact encounter streams + analysis).
# Repo root = directory containing crates/encounters. Total wall ~4 min on 8 vCPU.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"   # .../lab-1
OUT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
cargo build -p emergent-encounters --release --offline --example stream
S="$(cargo metadata --format-version 1 --offline --no-deps | python3 -c 'import json,sys;print(json.load(sys.stdin)["target_directory"])')/release/examples/stream"
cd "$OUT"
# lambda(sigma_e) sweep (5 points bracket the peak at sigma_e*a ~ W=0.08)
for se in 1e-3 3e-3 1e-2 3e-2 8e-2 1.5e-1; do
  $S "se$se" 500 "$se" 3e-3 0.96 1.04 0 400 20261002 > "belt_se$se.tsv" 2> "belt_se$se.err"
done
# fleet concentration: 8 exact-period keys (62 bodies per key)
$S fleet 500 3e-3 3e-3 0.96 1.04 8 400 20261002 > belt_fleet.tsv 2> belt_fleet.err
# second seed (robustness)
$S se3e-3b 500 3e-3 3e-3 0.96 1.04 0 400 20261003 > belt_se3e-3b.tsv 2> belt_se3e-3b.err
$S se1e-2b 500 1e-2 3e-3 0.96 1.04 0 400 20261003 > belt_se1e-2b.tsv 2> belt_se1e-2b.err
python3 analyze.py belt_*.tsv
python3 cascade.py
