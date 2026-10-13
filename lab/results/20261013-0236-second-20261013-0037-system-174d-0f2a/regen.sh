#!/bin/bash
# Regenerates every number in dossier.md for run 20261013-0236-second-20261013-0037-system-174d-0f2a
# (second author on 20261013-0037-system-174d). The runner applies work/patch.diff (the original
# probe plus this run's `clock_full`/`r_e6` extension, counters only, env-gated) before running this.
# Total wall time on the lab's Linux/x86 runner: ~2 min including the build.
set -e
cd "$(dirname "$0")/../../../crates/universe"

echo "== build =="
cargo build --release --example waterfall 2>&1 | tail -1

echo
echo "== decisive battery: paced 8 s (the checker's adversarial case), seed 1 =="
cargo run --release --example waterfall -- 100 8 2>/dev/null | grep -v "^kick tick"

echo
echo "== paced 4 s, seed 1 =="
cargo run --release --example waterfall -- 100 4 2>/dev/null | grep -v "^kick tick"

echo
echo "== paced 8 s, seed 7 (cross-seed) =="
cargo run --release --example waterfall -- 100 8 2 7 2>/dev/null | grep -v "^kick tick"

echo
echo "== demand 4 s, seed 1 (unlimited budget; 4 s so the turn flight's 2.5 s burn fires) =="
cargo run --release --example waterfall -- 100 4 demand 2>/dev/null | grep -v "^kick tick"

echo
echo "== summary table (kicks -> law-cadence events, per flight, from the paced-8s record) =="
cargo run --release --example waterfall -- 100 8 2>/dev/null | grep -v "^kick tick" | python3 -c "
import sys, re
cur = None
for ln in sys.stdin:
    if ln.startswith('=== '):
        cur = ln[4:].split('(')[0].strip()
    m = re.search(r'mints ~(\d+) events \(law-bound kicks (\d+), burn-bound (\d+)\)', ln)
    if m and cur:
        print(f'{cur}: law-cadence events {m.group(1)} (law-bound {m.group(2)}, burn-bound {m.group(3)})')
    k = re.search(r'for the same (\d+)/(\d+) thrust kicks', ln)
    if k and cur:
        print(f'{cur}: thrust kicks {k.group(1)}')
"
