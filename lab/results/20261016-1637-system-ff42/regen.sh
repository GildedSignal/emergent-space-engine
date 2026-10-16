#!/bin/sh
# Regenerates every number in dossier.md from shipped code + work/patch.diff (<= 15 min).
set -e
cd "$(dirname "$0")/../../.."   # repo root
git apply --allow-empty "$(dirname "$0")/work/patch.diff" 2>/dev/null || true
# The bench is an example in the patch; build and run it (answers, probes, cost).
cargo run --release -p emergent-universe --example levelbench 2>/dev/null | tee "$(dirname "$0")/bench.txt"
# One diagnostic case (the f=0.4 crash course): shows the folded periapsis, the readout
# radius at it, and the two answers agreeing.
cargo run --release -p emergent-universe --example levelbench -- diag 2>/dev/null | tee "$(dirname "$0")/diag.txt"
echo DONE
