#!/bin/sh
# Regenerates every number in dossier.md from shipped code + this run's edits.
# work/patch.diff (the runner's saved tree edits, incl. crates/lattice/examples/passthrough.rs)
# is applied before this runs. ~15 s total.
set -e
RUN="$(cd "$(dirname "$0")" && pwd)"
cd "$RUN/../../.."  # repo root
mkdir -p "$RUN/out"
cargo run --release -p emergent-lattice --example passthrough > "$RUN/out/passthrough.txt"
echo "--- key lines (full table in out/passthrough.txt) ---"
grep -E "boundary grid|misses|positive control|negative control|missile \+ 50 m ship, closing 0.9" "$RUN/out/passthrough.txt"
