#!/bin/sh
# Regenerates every number in dossier.md from shipped code + this run's scripts.
# Wall on the lab's 8-vCPU machine: ~10-13 min (the three n=12800 arms at
# horizon 24576 dominate; all seven arms run in parallel). Patch
# (work/patch.diff, adds crates/lattice/examples/breathe.rs) must be applied
# before this runs; base 52db369f (crates identical to 84b2's base 8d9e7f88).
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
# The gold-deciding arms (checker's named experiment): n = 12800 flown to
# extinction at horizon 24576 = 102 side-units (2.1x the 6400-relative horizon
# at which 6400 reached its baseline), seeds 1-3, keep 0. The same series also
# regenerates every truncated-horizon number (H 8192/12288) by analysis.
# Corrected record cells: the 6400 ladder row (3-seed values) and poly_r.
{
for s in 1 2 3; do
  echo "$B 12800 0.7 65536 $s 1024 24576 0 > $D/ext_n12800_s$s.csv"
done
echo "$B 400 0.7 65536 1 1024 8192 0 > $D/lad_n400_s1.csv"
echo "$B 1600 0.7 65536 1 1024 8192 0 > $D/lad_n1600_s1.csv"
for s in 1 2 3; do
  echo "$B 6400 0.7 65536 $s 1024 8192 0 > $D/lad_n6400_s$s.csv"
done
echo "$B 6400 0.7 65536 1 1024 8192 0 1 0.75,1 > $D/poly_r6400_s1.csv"
} | xargs -P 7 -I{} sh -c '{}'
python3 summary2.py | tee summary.txt
