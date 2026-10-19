#!/bin/sh
# Regenerates every number in dossier.md from shipped code + this run's scripts.
# ~6-10 min wall on 8 vCPU. Patch (work/patch.diff) must be applied first (adds
# crates/lattice/examples/breathe.rs).
set -e
RUN="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$RUN/../../.." && pwd)"   # repo root
B=/home/glmlab/lab-target-1/release/examples/breathe
if [ ! -x "$B" ]; then
  (cd "$ROOT" && cargo build --release -p emergent-lattice --example breathe)
fi
cd "$RUN"
D=data
mkdir -p $D
# N-ladder, seeds 1-3 (the identity table, block decay, periods, allocator ratios)
for n in 400 800 1600 3200 6400; do for s in 1 2 3; do
  echo "$B $n 0.7 65536 $s 1024 8192 0 > $D/lad_n${n}_s${s}.csv"
done; done | xargs -P 6 -I{} sh -c '{}'
# Dephasing (held-out P5): mass and radius spread at n = 6400, seed 1
$B 6400 0.7 65536 1 1024 8192 0 1,2,4 > $D/poly_m6400_s1.csv
$B 6400 0.7 65536 1 1024 8192 0 1 0.75,1 > $D/poly_r6400_s1.csv
# Long horizons: the ringdown never returns
$B 400 0.7 65536 1 1024 32768 0 > $D/long_n400_s1.csv
$B 400 0.7 65536 2 1024 32768 0 > $D/long_n400_s2.csv
$B 1600 0.7 65536 1 1024 32768 0 > $D/long_n1600_s1.csv
$B 3200 0.7 65536 1 1024 24576 0 > $D/long_n3200_s1.csv
python3 summary.py | tee summary.txt
