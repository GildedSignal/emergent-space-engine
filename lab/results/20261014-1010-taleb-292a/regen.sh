#!/bin/sh
# Regen for 20261014-1010-taleb-292a: every dossier number, from shipped code
# + work/patch.diff (adds crates/universe/examples/seam_cycle.rs). < 2 min.
set -e
cd "$(dirname "$0")/../../.."   # repo root
RUN=lab/results/20261014-1010-taleb-292a
cargo run --release -p emergent-universe --example seam_cycle -- "$RUN/seam.json" | tee "$RUN/probe-stdout.txt"
python3 "$RUN/analyze.py" "$RUN/seam.json" | tee "$RUN/analysis.txt"
