#!/bin/sh
# Regen: every dossier number from shipped code + this run's scripts (work/patch.diff applied first by the runner).
set -e
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261019-2339-fermi-f623

# 1. build the probe example (the only tree change; shipped nladder untouched)
cargo build --release -p emergent-universe --example alloc_probe
B=${CARGO_TARGET_DIR:-target}/release/examples/alloc_probe

# 2. allocator floor bench (x86 glibc; orders of magnitude only)
cd "$R"
rustc -O bench_malloc.rs -o bench_malloc
./bench_malloc 5000000 | tee bench_out.txt

# 3. the two coast arms (each <= 30 s wall, < 200 MB RSS)
"$B" 10000 coast 25 2000 12 > arm_1e4_coast.log 2>&1
"$B" 30000 coast 20 2000 12 > arm_3e4_coast.log 2>&1

# 4. composition (per-kick laws, attribution, the after-lever table)
python3 compose.py | tee compose_out.txt
echo "regen done"
