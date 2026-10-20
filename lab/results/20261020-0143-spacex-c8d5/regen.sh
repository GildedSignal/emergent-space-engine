#!/usr/bin/env bash
# Regenenerates every number in dossier.md from the shipped tree + work/patch.diff.
# The patch carries: the env-gated keep dial (universe.rs), the binding_at census (body.rs),
# and the keep_probe example. ~6 min on the lab box (8 vCPU), every process < 2 GB.
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root

# Apply the run's patch unless the tree already carries the edits (then this is a no-op).
PATCH=lab/results/20261020-0143-spacex-c8d5/work/patch.diff
if [ -f "$PATCH" ] && ! grep -q "ES_KEEP_LEGS" crates/universe/src/universe.rs; then
  git apply "$PATCH" || true
fi
cargo build --release -p emergent-universe --example keep_probe
B=${CARGO_TARGET_DIR:-target}/release/examples/keep_probe
L=lab/results/20261020-0143-spacex-c8d5/logs-regen
mkdir -p "$L"

# The six arms (each prints one block: view completeness, census, memory).
$B 10000 coast 5 6000 2  | tee "$L/stock_coast.txt"
ES_KEEP_LEGS=1 $B 10000 coast 5 6000 2  | tee "$L/oneleg_coast.txt"
$B 10000 coast 5 6000 60 | tee "$L/stock_sparse.txt"
ES_KEEP_LEGS=1 $B 10000 coast 5 6000 60 | tee "$L/oneleg_sparse.txt"
$B 10000 burn 5 6000 2   | tee "$L/stock_burn.txt"
ES_KEEP_LEGS=1 $B 10000 burn 5 6000 2   | tee "$L/oneleg_burn.txt"

# Digest wall-coupling control: the same stock arm, run again — same args, drift digest.
$B 10000 coast 5 6000 2  | tee "$L/stock_coast_again.txt"

echo "REGEN DONE: compare $L against logs/ (see dossier: same-args digest drift is the point of stock_coast_again)"
