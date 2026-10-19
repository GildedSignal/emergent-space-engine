#!/bin/sh
# Regenerates every number in dossier.md from shipped code + this run's patch
# (work/patch.diff: the gravitybelt harness extended with --pass/--every, plus the
# gravityorbit isolated-ladder example). One process at a time (shared machine,
# <2 GB each). Total wall time observed: ~9 min on 8 vCPU Linux.
set -e
cd "$(dirname "$0")/../../.."   # repo root
R=$(pwd)
RUN=$R/lab/results/20261019-1656-second-20261019-1551-dynamics-e3b7-9b3b

# 1. Apply the harness patch if the examples are not already present (idempotent).
if [ ! -f crates/lattice/examples/gravityorbit.rs ] || ! grep -q '"--pass"' crates/lattice/examples/gravitybelt.rs; then
  git apply "$RUN/work/patch.diff"
fi

# 2. Build.
cargo build --release --example gravitybelt --example gravityorbit -p emergent-lattice
B=$R/target/release/examples/gravitybelt
O=$R/target/release/examples/gravityorbit
[ -x "$B" ] || B=/home/glmlab/lab-target-0/release/examples/gravitybelt
[ -x "$O" ] || O=/home/glmlab/lab-target-0/release/examples/gravityorbit

mkdir -p "$RUN/work"
# 3. The original ladder (digests must equal the author's and the checker's:
#    G_s1 e3462444, C_s1 634d9918, GW 79b89629, G_s2 420ef2ff, C_s2 e903ff6d,
#    C0 e8a69ff7).
"$B" --n 1600 --seed 1 --horizon 49152 --slim --out "$RUN/work/G_s1_h49152.tsv" 2>/dev/null
"$B" --n 1600 --seed 1 --horizon 49152 --nofleet --slim --out "$RUN/work/C_s1_h49152.tsv" 2>/dev/null
"$B" --n 1600 --seed 1 --horizon 24576 --boxhalf 150 --slim --out "$RUN/work/GW_s1_h24576.tsv" 2>/dev/null
"$B" --n 1600 --seed 2 --horizon 16384 --slim --out "$RUN/work/G_s2_h16384.tsv" 2>/dev/null
"$B" --n 1600 --seed 2 --horizon 16384 --nofleet --slim --out "$RUN/work/C_s2_h16384.tsv" 2>/dev/null
"$B" --n 1600 --seed 1 --horizon 16384 --nofleet --thermal 0 --slim --out "$RUN/work/C0_s1_h16384_thermal0.tsv" 2>/dev/null

# 4. The named experiment (Pass controls) and the cadence arm (digests must equal
#    the checker's independent flights: A1 b73b06dc, A4 e98306bb).
"$B" --n 1600 --seed 1 --horizon 32768 --nofleet --thermal 0 --pass --slim --out "$RUN/work/A1_C0s1_h32768_pass.tsv" 2>/dev/null
"$B" --n 1600 --seed 1 --horizon 49152 --nofleet --thermal 0 --pass --slim --out "$RUN/work/A2_C0s1_h49152_pass.tsv" 2>/dev/null
"$B" --n 1600 --seed 1 --horizon 49152 --nofleet --pass --slim --out "$RUN/work/A3_Cs1_h49152_pass.tsv" 2>/dev/null
"$B" --n 1600 --seed 1 --horizon 16384 --nofleet --thermal 0 --every 4 --slim --out "$RUN/work/A4_C0s1_h16384_every4.tsv" 2>/dev/null

# 5. The isolated-orbit eccentricity ladder (98304 ch = 14 orbits at a=70q).
for e in 0 0.01 0.06 0.2 0.5 0.8 0.97 0.975 0.98 0.985 0.99; do
  "$O" --a 70 --e $e --horizon 98304 --out "$RUN/work/O_a70_e$e.tsv" 2>/dev/null
done
"$O" --a 36 --e 0 --horizon 98304 --out "$RUN/work/O_a36_e0.tsv" 2>/dev/null
"$O" --a 36 --e 0.5 --horizon 98304 --out "$RUN/work/O_a36_e0.5.tsv" 2>/dev/null
"$O" --a 70 --e 0 --dv 1 --horizon 98304 --out "$RUN/work/O_a70_dv1.tsv" 2>/dev/null

# 6. Analysis -> work/analysis2.json (printed; digest_expect_ok must be all true).
python3 "$RUN/analyze2.py"
