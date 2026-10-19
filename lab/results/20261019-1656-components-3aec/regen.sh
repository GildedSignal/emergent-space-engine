#!/usr/bin/env bash
# Regenerates every dossier number from shipped code + work/patch.diff (<= 15 min total).
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root
RUN=lab/results/20261019-1656-components-3aec
git apply --allow-empty "$RUN/work/patch.diff" 2>/dev/null || true   # nladder Linux footprint stub
cargo build --release -p emergent-universe --example nladder --example belt_first
cargo build --release -p emergent-universe --example nladder --features prof
BIN="$CARGO_TARGET_DIR/release/examples"; BIN="${BIN:-/home/glmlab/lab-target-1/release/examples}"
{ "$BIN/nladder" 10000 coast 10; "$BIN/nladder" 100000 coast 10; "$BIN/belt_first" 10000; } > "$RUN/work/probes.log" 2>&1
"$BIN/nladder" 100000 coast 10 > "$RUN/work/prof1e5.log" 2>&1
"$BIN/nladder" 10000  coast 10 > "$RUN/work/prof1e4.log" 2>&1
python3 "$RUN/ledger.py"
