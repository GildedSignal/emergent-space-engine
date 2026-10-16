#!/bin/bash
# Regenerates every number in dossier.md. No tree edits: work/patch.diff is empty,
# the run only adds files in its own folder. Total under 5 minutes on 2 GB.
set -e
cd "$(dirname "$0")"

echo "== anchor: the shipped belt_first example (source: crates/universe/examples/belt_first.rs)"
echo "== prints the belt's first-kick times in game-s; interval = 2 x p50 (kick at mid-step)"
cargo run --release -p emergent-universe --example belt_first 2>&1 | tee belt_first.out

echo ""
echo "== the closing ledger (arithmetic from page-cited constants)"
python3 ledger.py 2>&1 | tee ledger.out

echo ""
echo "== checks the dossier's claims rest on:"
python3 - <<'EOF'
import re
out = open("belt_first.out").read()
m = re.search(r"belt: (\d+) bodies, first item \(game s\) min (\d+) p01 (\d+) p50 (\d+)", out)
assert m, "belt_first output not parsed"
p50 = int(m.group(4))
print(f"belt first-kick p50 {p50} game-s -> interval {2*p50} s (recorded 28,141.5; pred P1: 14,100+-700: {'HELD' if abs(p50-14100)<=700 else 'FAILED'})")
kepler = 2*3.141592653589793*(35_600_000/0.9)**1.5*4.925490947e-6
pd = 2*p50*128
print(f"P_D implied {pd:.3e} s = {pd/kepler:.3f} x Cinder's SI Kepler period {kepler:.3e} s (pred P2: 0.468+-0.02: {'HELD' if abs(pd/kepler-0.468)<=0.02 else 'FAILED'})")
led = open("ledger.out").read()
for want in ["177.50 cores", "0.17 cores", "8.65 cores", "23.1 us", "69 s", "62-571", "1.19e+06-1.65e+06"]:
    assert want in led, f"ledger missing {want}"
print("ledger spot-checks: all present")
EOF
