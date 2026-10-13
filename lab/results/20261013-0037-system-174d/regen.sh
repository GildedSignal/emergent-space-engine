#!/bin/bash
# Regenerates every number in dossier.md for run 20261013-0037-system-174d.
# The runner applies work/patch.diff (the probe in step.rs + this example) before running this.
# Total wall time on the lab's Linux/x86 runner: ~3 min (build included).
set -e
cd "$(dirname "$0")/../../../crates/universe"

echo "== build =="
cargo build --release --example waterfall 2>&1 | tail -1

echo
echo "== the decomposition, paced (12 ms frame budget, the sweep's flight conditions) =="
cargo run --release --example waterfall -- 100 4 2>/dev/null | grep -v "^kick tick"

echo
echo "== the decomposition, demand mode (unlimited budget: every due item in its frame) =="
cargo run --release --example waterfall -- 100 2 demand 2>/dev/null | grep -v "^kick tick"

echo
echo "== cadence-law check over every thrust kick (demand run) =="
cargo run --release --example waterfall -- 100 2 demand 2>/dev/null | grep "^kick tick" | python3 -c "
import sys, math, statistics
TL = -44  # Config::default().thrust_log2 (crates/universe/src/ctx.rs:42)
total = mismatch = 0
rs = []
for ln in sys.stdin:
    p = ln.split()
    step, beta, tq, bq = int(p[4]), float(p[6]), int(p[8]), int(p[10])
    if bq <= 0:
        continue
    total += 1
    rs.append((tq + 1) / (bq + 1))
    ok = False
    for L in range(16):
        ticks = beta * 2**-6 / 2.0**(TL + L)
        pred = max(128, min(2**50, 2**int(math.floor(math.log2(ticks)))))
        if pred == step:
            ok = True
            break
    mismatch += not ok
rs.sort()
print(f'thrust kicks {total}; cadence-formula mismatches {mismatch} (alignment/MIN_STEP remainders)')
print(f'tide/burn dv ratio: min {rs[0]:.3e} median {statistics.median(rs):.3e} max {rs[-1]:.3e}')
"
