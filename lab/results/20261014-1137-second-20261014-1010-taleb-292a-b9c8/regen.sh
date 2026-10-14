#!/bin/sh
# Regen for 20261014-1137-second-20261014-1010-taleb-292a-b9c8: every dossier number,
# from shipped code + work/patch.diff (adds crates/universe/examples/seam_cycle.rs, the
# corrected probe). Runtime ~25 s once built; first build may take ~1-2 min.
set -e
cd "$(dirname "$0")/../../.."   # repo root
RUN=lab/results/20261014-1137-second-20261014-1010-taleb-292a-b9c8
# The runner applies work/patch.diff before this runs; apply it ourselves if not yet.
if [ ! -f crates/universe/examples/seam_cycle.rs ]; then
  git apply "$RUN/work/patch.diff"
fi
cargo run --release -p emergent-universe --example seam_cycle -- "$RUN/seam2.json" 256 | tee "$RUN/probe-stdout.txt"
python3 "$RUN/analyze.py" "$RUN/seam2.json" | tee "$RUN/analysis.txt"
