#!/usr/bin/env bash
# Regen: rebuild the genesis example from the patch, rerun the three flights, recompute the dossier's numbers.
# ~7 min total. Patch = work/patch.diff (the genesis example + Universe::stagger_genesis).
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root (the runner applies work/patch.diff before this runs)
cargo build --release -p emergent-universe --example genesis
D="$(cd "$(dirname "$0")" && pwd)"
T="$(mktemp -d)"
BIN="${CARGO_TARGET_DIR:-target}/release/examples/genesis"
"$BIN" ship 3000 24 1   > "$T/ship_seed1_gens24.log" 2>&1
"$BIN" stagger 3000 14 1 > "$T/stagger_seed1_gens14.log" 2>&1
"$BIN" ship 3000 14 2   > "$T/ship_seed2_gens14.log" 2>&1
cp "$T"/*.log "$D"/
python3 "$D/analyze.py" "$D/ship_seed1_gens24.log" "$D/stagger_seed1_gens14.log" "$D/ship_seed2_gens14.log"
