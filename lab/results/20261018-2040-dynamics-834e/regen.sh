#!/usr/bin/env bash
# Regenerates every number in dossier.md. Applies work/patch.diff (the harness
# crates/lattice/examples/fill.rs) first, then runs the fill ladder and the analysis.
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root
git apply --allow-empty "$(dirname "$0")/work/patch.diff" 2>/dev/null || git apply --reject "$(dirname "$0")/work/patch.diff" || true
cargo build --release -p emergent-lattice --example fill
cargo run --release -p emergent-lattice --example fill -- all > "$(dirname "$0")/fill.jsonl" 2>/dev/null
python3 "$(dirname "$0")/analyze.py" "$(dirname "$0")/fill.jsonl" | tee "$(dirname "$0")/analysis.txt"
