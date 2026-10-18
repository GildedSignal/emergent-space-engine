#!/usr/bin/env bash
# Regenerates every number in dossier.md (20261018-2155-quant-34be).
# The u64-port pricing bench lives in the run's patch (work/patch.diff applies it).
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root (lab/results/<run>/regen.sh)
cargo build --release -p emergent-encounters --example quant_u64
# The shipped exactness tests of the function being ported (positive control).
cargo test --release -p emergent-encounters -- dioph 2>&1 | tail -3
# The decisive run: brute spot-check, census/identity, three-way interleaved timing.
./target/release/examples/quant_u64 2>/dev/null || "$CARGO_TARGET_DIR/release/examples/quant_u64"
