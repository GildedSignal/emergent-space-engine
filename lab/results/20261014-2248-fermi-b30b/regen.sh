#!/usr/bin/env bash
# Regenerates every number in dossier.md. ~4-5 min of runs after the build.
# Shipped main + work/patch.diff (adds examples/wave_steady.rs; no shipped path touched).
set -euo pipefail
cd "$(dirname "$0")/../../.."  # repo root
RUN=lab/results/20261014-2248-fermi-b30b

if [ ! -f crates/universe/examples/wave_steady.rs ]; then git apply "$RUN/work/patch.diff"; fi
cargo build --release -p emergent-universe --example wave_steady 2>&1 | tail -1
B=$(ls target/release/examples/wave_steady 2>/dev/null || echo ${CARGO_TARGET_DIR:-/nonexistent}/release/examples/wave_steady)
[ -x "$B" ] || B=$(find "${CARGO_TARGET_DIR:-target}" -type f -name wave_steady | head -1)
mkdir -p "$RUN/out"

# Validity (P6): digest must be identical across chunkings at each cut.
"$B" 10000 2500 100 1 2500 | tail -1 | tee "$RUN/out/valid_rtf100_cut2500.txt"
"$B" 10000 2500 6000 1 2500 | tail -1 | tee "$RUN/out/valid_rtf6000_cut2500.txt"
"$B" 10000 16000 600 1 2000 | tail -1 | tee "$RUN/out/valid_rtf600_cut16000.txt"
"$B" 10000 16000 6000 1 2000 | tail -1 | tee "$RUN/out/valid_rtf6000_cut16000.txt"

# The four arms (decisive run first).
"$B" 100000 115000 6000 1 2500 > "$RUN/out/n1e5_seed1_rtf6000.txt"   # ~50 s
"$B" 30000 115000 6000 1 2500 > "$RUN/out/n3e4_seed1.txt"            # ~27 s
"$B" 200000 60000 6000 1 2500 > "$RUN/out/n2e5_seed1.txt"            # ~36 s
"$B" 100000 60000 6000 2 2500 > "$RUN/out/n1e5_seed2.txt"            # ~31 s

python3 "$RUN/analyze.py"
