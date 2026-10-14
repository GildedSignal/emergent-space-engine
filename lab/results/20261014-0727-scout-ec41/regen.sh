#!/usr/bin/env bash
# Regen (20261014-0727-scout-ec41): every dossier number from shipped code + work/patch.diff.
# ~2 min. Requires the workspace Cargo build (CARGO_TARGET_DIR default of this checkout).
set -euo pipefail
cd "$(dirname "$0")/../../.."
OUT="$(dirname "$0")/work"
mkdir -p "$OUT"

# The patch adds crates/encounters/examples/cycle.rs (applied by the runner before this runs).
cargo build --release -p emergent-encounters --example cycle 2>&1 | tail -1
BIN=$(cargo metadata --no-deps --format-version 1 | tr ',' '\n' | sed -n 's/"target_directory":"\(.*\)"/\1/p')/release

# Shipped grounding: kick (single-kick slack/budget/violations), scale n (degree law,
# encounter-rate constancy), steady (horizon amortization). ~75 s.
"$BIN/encounters" kick        | tee "$OUT/shipped.jsonl"
"$BIN/encounters" scale n     | tee -a "$OUT/shipped.jsonl"
"$BIN/encounters" steady 10000 1e-4 10 100 1000 | tee -a "$OUT/shipped.jsonl"

# This run's probe: cumulative kick streams (co/random-walk), renewal-on-failure rate,
# cut vs per-kick, checks per renewal, first-change distribution. ~18 s. Args: n rho sigma_e seed bodies.
"$BIN/examples/cycle" 10000 1e-4 1e-2 20261050 30 | tee "$OUT/cycle.jsonl"

echo "regen done: $OUT/shipped.jsonl $OUT/cycle.jsonl"
