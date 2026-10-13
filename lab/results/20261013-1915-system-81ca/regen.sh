#!/bin/sh
# Regenerates every number in dossier.md for run 20261013-1915-system-81ca.
# work/patch.diff (applied by the runner before this runs) adds crates/space/tests/carlson_probe.rs.
set -e
RUN_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$RUN_DIR/../../.."   # repo root (lab/results/<id> -> root)
cargo test --release -p emergent-space --test carlson_probe -- --nocapture 2>&1 | tee "$RUN_DIR/probe-out.txt"
echo "Done. Numbers are in probe-out.txt (STRONG/WEAK/HELD-OUT summary lines and the tables)."
