#!/usr/bin/env bash
# Regenerates every number in dossier.md from the shipped tree + work/patch.diff (applied first).
# The patch carries: the keep dial (ES_KEEP_LEGS, universe.rs), the binding_at census (body.rs),
# the drop census + the env-gated view clamp (ES_VIEW_CLAMP, view.rs), and the keep_probe2
# example (per-gather completeness with per-id attribution). ~5 min on the lab box, each
# process < 2 GB.
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root

PATCH=lab/results/20261020-2004-spacex-26fc/work/patch.diff
if [ -f "$PATCH" ] && ! grep -q "keepcensus" crates/universe/src/body.rs; then
  git apply "$PATCH" || true
fi
cargo build --release -p emergent-universe --example keep_probe2
B=${CARGO_TARGET_DIR:-target}/release/examples/keep_probe2
L=lab/results/20261020-2004-spacex-26fc/logs-regen
mkdir -p "$L"

# Bench-depth arms: stock, the clamp fix (no-op control), the one-leg keep.
$B 10000 coast 5 6000 2  | tee "$L/stock_coast.txt"
ES_VIEW_CLAMP=1 $B 10000 coast 5 6000 2  | tee "$L/clamp_coast.txt"
ES_KEEP_LEGS=1 $B 10000 coast 5 6000 2   | tee "$L/oneleg_coast.txt"

# Deep arms (coast, gather every 300 frames): attribution and memory at ~10^5 game-s, both keeps.
$B 10000 coast 60 6000 300 | tee "$L/stock_coast_deep.txt"
ES_KEEP_LEGS=1 $B 10000 coast 60 6000 300 | tee "$L/oneleg_coast_deep.txt"

echo "REGEN DONE: compare $L against logs/ (the 'drop dead'/'drop none' lines carry the
attribution; grep -v '^drop ' for the summary lines). Same-args digest drift is the known
wall coupling (c8d5) — completeness and attribution lines are the certificate, not digests."
