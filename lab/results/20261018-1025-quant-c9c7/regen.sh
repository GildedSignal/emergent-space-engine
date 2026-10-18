#!/bin/sh
# Regenerates every number in dossier.md (work/churn.jsonl) in < 2 min on 8 vCPU/15 GB.
# work/patch.diff (the churn example + the parameterized `encounters kick`) is applied
# before this runs; if not, apply it first. Run folder is lab/results/<id>, 3 levels
# below the repo root.
set -e
R="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$R/../../.." && pwd)"
cd "$ROOT"
if [ ! -f crates/encounters/examples/churn.rs ]; then
  git apply "$R/work/patch.diff"
fi
cargo build --release -p emergent-encounters --example churn --bin encounters >/dev/null 2>&1
B="${CARGO_TARGET_DIR:-target}/release/examples/churn"
K="${CARGO_TARGET_DIR:-target}/release/encounters"
{
  # The law: fixed band [2,3), belt mix sigma_R = 0.07, quantum kick eps = 2^-23.
  $B 10000 0.07 2 3 20261050 64
  $B 30000 0.07 2 3 20261050 64
  $B 100000 0.07 2 3 20261050 64
  $B 300000 0.07 2 3 20261050 64
  $B 1000000 0.07 2 3 20261050 24
  # Dispersion control: sigma_R = 0.01 (unsaturated regime).
  $B 100000 0.01 2 3 20261050 64
  # fe6b's own spec anchors (sigma 1e-2, band [1,1.5]) at both N ends.
  $B 10000 0.01 1 1.5 20261050 64
  $B 1000000 0.01 1 1.5 20261050 24
  # Fixed-density control (4e4/AU^2, the 1e6-in-[2,3) anchor's density).
  $B 300000 0.07 2 2.527306 20261050 64
  # Held-out seed 777.
  $B 100000 0.07 2 3 777 48
  $B 300000 0.07 2 2.527306 777 48
  # The slack arm: the shipped `kick` experiment (now parameterized), belt mix,
  # quantum eps + burn-class controls, and N / seed arms.
  $K kick 10000 0.07 1e-4 2 3 20261050 24 1.1920928955078125e-7 1e-5 1e-3
  $K kick 30000 0.07 1e-4 2 3 20261050 16 1.1920928955078125e-7
  $K kick 10000 0.07 1e-4 2 3 777 24 1.1920928955078125e-7
} > "$R/work/churn.jsonl"
cat "$R/work/churn.jsonl"
