#!/bin/sh
# Regenerates every number in dossier.md from shipped code + work/patch.diff (already applied
# by the runner). Builds the example, freezes a private binary (a sibling rebuild of the shared
# target must not contaminate the flights), flies the six-scene × three-arm matrix, and prints
# the identity verdict. Total ≈ 13 min on the 8-vCPU box (build 1 min, matrix ≈ 12 min).
set -e
cd "$(dirname "$0")/../../.." || exit 1
R="$(pwd)/lab/results/20261015-1747-second-20261015-1615-spacex-1343-3dc8"

echo "== build =="
cargo build --release -p emergent-universe --example passage_demote

echo "== freeze a private binary (contamination defense) =="
BIN="$R/work/bin/passage_demote"
mkdir -p "$R/work/bin"
cp "${CARGO_TARGET_DIR:-$PWD/target}/release/examples/passage_demote" "$BIN"

echo "== the decisive matrix =="
sh "$R/matrix.sh" "$R" "$BIN" | tee "$R/regen.log"
