#!/bin/sh
# Regenerates every number in dossier.md from shipped code + this run's patch.
# Applies work/patch.diff (the gravitybelt harness), rebuilds, flies the ladder,
# runs the analysis. Total wall time observed: ~8-10 min on 8 vCPU Linux.
set -e
cd "$(dirname "$0")/../../.."   # repo root
R=$(pwd)
RUN=$R/lab/results/20261019-1551-dynamics-e3b7

# 1. Apply the harness patch if the example is not already present (the runner's
#    clean tree needs it; idempotent).
if [ ! -f crates/lattice/examples/gravitybelt.rs ]; then
  git apply "$RUN/work/patch.diff"
fi

# 2. Build (target dir is shared/persistent under the lab; ~4 s incremental).
cargo build --release --example gravitybelt -p emergent-lattice
B=$R/target/release/examples/gravitybelt
[ -x "$B" ] || B=/home/glmlab/lab-target-3/release/examples/gravitybelt

# 3. The ladder (same commands as the run; one process at a time).
mkdir -p "$RUN/work"
"$B" --n 1600 --seed 1 --horizon 49152 --slim --out "$RUN/work/G_s1_h49152.tsv" 2>/dev/null
"$B" --n 1600 --seed 1 --horizon 49152 --nofleet --slim --out "$RUN/work/C_s1_h49152.tsv" 2>/dev/null
"$B" --n 1600 --seed 1 --horizon 24576 --boxhalf 150 --slim --out "$RUN/work/GW_s1_h24576.tsv" 2>/dev/null
"$B" --n 1600 --seed 2 --horizon 16384 --slim --out "$RUN/work/G_s2_h16384.tsv" 2>/dev/null
"$B" --n 1600 --seed 2 --horizon 16384 --nofleet --slim --out "$RUN/work/C_s2_h16384.tsv" 2>/dev/null
"$B" --n 1600 --seed 1 --horizon 16384 --nofleet --thermal 0 --slim --out "$RUN/work/C0_s1_h16384_thermal0.tsv" 2>/dev/null

# 4. Analysis -> work/analysis.json (printed).
python3 "$RUN/analyze.py"
