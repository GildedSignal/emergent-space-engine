#!/bin/bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff.
# Linux/x86 cloud: orders of magnitude only (the integrator re-measures on the M1).
# Total wall: ~3.5 min (arm D alone is ~66 s and peaks 2.4 GB RSS; skip it with QUICK=1).
set -e
cd "$(dirname "$0")/../../.." || exit 1
if [ ! -f crates/universe/examples/scanpre.rs ]; then git apply lab/results/20261021-1551-spacex-eb24/work/patch.diff; else echo "(patch already applied)"; fi
cargo build --release -p emergent-universe --example scanpre 2>&1 | grep -E "^error" -A4 || true
B=${CARGO_TARGET_DIR:-target}/release/examples/scanpre
[ -x "$B" ] || B=/home/glmlab/lab-target-3/release/examples/scanpre

echo "== clock-pair calibration (the lookup split's bias, subtract 36 ns per timed call)"
cat > /tmp/clkcal.rs <<'EOF'
use std::time::Instant;
fn main() {
    let n = 5_000_000u64;
    let t = Instant::now();
    let mut acc = 0u64;
    for _ in 0..n {
        let a = Instant::now();
        acc = acc.wrapping_add(a.elapsed().as_nanos() as u64);
    }
    println!("clock pair (now+elapsed): {:.1} ns (checksum {acc})", t.elapsed().as_nanos() as f64 / n as f64);
}
EOF
rustc -O /tmp/clkcal.rs -o /tmp/clkcal && /tmp/clkcal

run() { echo "== $*"; if [ -n "$PRE" ]; then ES_SCAN_SPLIT=1 ES_SCAN_PRECHECK=$PRE "$B" "$@" | tail -2; else ES_SCAN_SPLIT=1 "$B" "$@" | tail -2; fi; }

# Attribution + digest controls (pre off vs the three pre-check forms, digest must not move)
run 3000 coast 20 100
run 30000 coast 20 100
run 100000 burn 20 100
for PRE in 1 2 3; do run 100000 burn 20 100; done   # v1 global epoch, v2 per-row+reg epochs, v3 value-me + epochs
if [ -z "$QUICK" ]; then run 100000 burn 20 2000; fi # the wall arm: the wave-era capture bail
