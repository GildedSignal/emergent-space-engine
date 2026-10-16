#!/bin/sh
# Regen: every dossier number, from shipped code and this run's scripts, <= 15 min.
set -e
cd "$(dirname "$0")/../../.."   # repo root (results/<run>/regen.sh)

# 1. The decisive arithmetic (pure, from shipped source constants; <= 1 s).
python3 lab/results/20261016-1319-fermi-1051/work/legality.py \
  > lab/results/20261016-1319-fermi-1051/work/legality.out

# 2. The constants exist on the shipped tree exactly as the script copies them.
grep -q "mass_log2: -18" crates/universe/src/scenario.rs
grep -q "periapsis: 260_000" crates/universe/src/scenario.rs || grep -q "260_000i128" crates/universe/src/scenario.rs
grep -q "5_200u128" crates/universe/src/scenario.rs
grep -q "periapsis: 35_600_000" crates/universe/src/scenario.rs
grep -q "step_log2: 7" crates/universe/src/ctx.rs
grep -q "pub const AU: i64 = 101_300_000" crates/universe/src/scenario.rs

# 3. The Linux anchor refusal (the flight claim's ground).
grep -q proc_pid_rusage crates/universe/examples/nladder.rs && echo "nladder: macOS-only (proc_pid_rusage) - anchor flight refused on Linux, as the dossier states"

cat lab/results/20261016-1319-fermi-1051/work/legality.out

# 4. The one Linux-clean anchor flight (N=0 plane, exodus frame), <= 60 s.
cargo build --release -p emergent-universe --example exodus >/dev/null 2>&1 || true
E=$(ls -1 target/release/examples/exodus /home/glmlab/lab-target-1/release/examples/exodus 2>/dev/null | head -1)
[ -n "$E" ] && timeout 35 "$E" 2>&1 | head -3
