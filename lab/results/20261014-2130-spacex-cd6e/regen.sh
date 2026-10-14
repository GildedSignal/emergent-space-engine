#!/bin/sh
# Regenerates every number in the dossier. ~6 min on the lab box (8 vCPU, shared).
# 1. apply the run's tree patch (the Rust example probe) if present
# 2. build + run the shipped readout probe (timing + verification dump)
# 3. verify the closed form against the shipped walk's dumped states
set -e
cd "$(dirname "$0")/../../.."   # repo root (lab/results/<run>/regen.sh)
if [ -f "lab/results/20261014-2130-spacex-cd6e/work/patch.diff" ] && [ ! -f crates/space/examples/readout_price.rs ]; then
  git apply lab/results/20261014-2130-spacex-cd6e/work/patch.diff
fi
cargo build --release --example readout_price -p emergent-space 2>&1 | tail -1
RUN=lab/results/20261014-2130-spacex-cd6e
"${CARGO_TARGET_DIR:-/home/glmlab/lab-target-2}/release/examples/readout_price" > "$RUN/shipped_dump.txt" 2>&1
grep "^KEY" "$RUN/shipped_dump.txt" | awk -F'read_ns=' '{print $2}' | sort -n | \
  awk '{a[NR]=$1} END{print "shipped read_ns: min",a[1],"p50",a[int(NR/2)],"max",a[NR],"of",NR,"keys"}'
grep "^KEY" "$RUN/shipped_dump.txt" | awk -F'build_us=' '{split($2,a," ");print a[1]}' | sort -n | \
  awk '{b[NR]=$1} END{print "shipped build_us: min",b[1],"p50",b[int(NR/2)],"max",b[NR]}'
# the I2 Hermite reduction against mpmath.quad (physics sanity)
cd "$RUN" && python3 closed_form_check.py
# full-grid verification against the shipped walk (slower, mpmath 30 dps)
python3 verify.py shipped_dump.txt
