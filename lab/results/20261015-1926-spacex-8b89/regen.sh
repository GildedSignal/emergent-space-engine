#!/bin/sh
# Regenerates every number in dossier.md from shipped code + work/patch.diff (already applied
# by the runner). Builds the example, freezes a private binary (a sibling rebuild of the shared
# target must not contaminate the flights), flies the matrix, prints the identity verdict.
# Total ≈ 8 min on the 8-vCPU box (build ~40 s, matrix ≈ 7 min).
set -e
cd "$(dirname "$0")/../../.." || exit 1
R="$(pwd)/lab/results/20261015-1926-spacex-8b89"

echo "== build =="
cargo build --release -p emergent-universe --example passage_demote

echo "== freeze a private binary (contamination defense) =="
T="$(cargo metadata --format-version 1 | tr ',' '\n' | sed -n 's/.*"target_directory":"\([^"]*\)".*/\1/p' | head -1)"
BIN="$R/work/bin/passage_demote"
mkdir -p "$R/work/bin"
cp "$T/release/examples/passage_demote" "$BIN"

echo "== the decisive matrix =="
sh "$R/matrix.sh" "$R" "$BIN" | tee "$R/regen.log"
