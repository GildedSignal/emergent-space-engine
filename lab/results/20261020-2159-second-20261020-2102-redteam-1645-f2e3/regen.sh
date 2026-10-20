#!/bin/sh
# Regen for 20261020-2159-second-20261020-2102-redteam-1645-f2e3.
# The runner applies work/patch.diff (adds crates/space/tests/kerr_view_probe.rs,
# the original run's probe, reused verbatim) before this runs. As a belt-and-braces
# measure the probe is also materialized verbatim from this folder (kerr_view_probe.rs,
# byte-identical to work/patch.diff's payload), so regen does not depend on the
# patch having been applied. Whatever this script creates, it removes again.
# Total: ~12 s (python) + cargo (warm ~5 s; first build may take minutes).
set -e
cd "$(dirname "$0")"
RUNDIR="$(pwd)"

python3 kerr_shadow2.py > instrument-out.txt

# Materialize the probe (idempotent; cleans up after itself).
PROBE=../../../crates/space/tests/kerr_view_probe.rs
CREATED=0
if [ ! -f "$PROBE" ]; then
    cp kerr_view_probe.rs "$PROBE"
    CREATED=1
fi
cleanup() {
    if [ "$CREATED" = 1 ] && [ -f "$PROBE" ]; then
        rm -f "$PROBE"
    fi
}
trap cleanup EXIT INT TERM

( cd ../../../crates/space && \
  cargo test -p emergent-space --test kerr_view_probe -- --nocapture 2>"$RUNDIR"/cargo-stderr.log \
  | grep -E "^DEFL" ) > shipped-defl.txt

# The shipped comparison is a dossier claim: it must be present, not silently empty.
if ! grep -q "^DEFL" shipped-defl.txt; then
    echo "FAIL: shipped-defl.txt has no DEFL lines (see cargo-stderr.log)" >&2
    exit 1
fi

echo "== shipped vs oracle residual (expect exactly |b|e-5 = 2b/r_max tail) =="
python3 - <<'PYEOF'
import re
ora = {}
for line in open('instrument-out.txt'):
    m = re.match(r'ORACLE a=([\d.]+) b=([+-][\d.]+) phi=([\d.]+|CAPTURED)', line)
    if m:
        ora[(float(m.group(1)), float(m.group(2)))] = m.group(3)
ship = {}
for line in open('shipped-defl.txt'):
    m = re.match(r'DEFL a=([\d.]+) b=([+-][\d.]+) (?:phi=([\d.]+)|CAPTURED)', line)
    if m:
        ship[(float(m.group(1)), float(m.group(2)))] = m.group(3)
both = set(ora) & set(ship)
dis = [k for k in both if (ora[k] == 'CAPTURED') != (ship[k] is None)]
caps = sum(1 for k in both if ora[k] == 'CAPTURED')
worst = 0.0
n = 0
for k in both:
    if ora[k] != 'CAPTURED' and ship[k] is not None:
        worst = max(worst, abs(float(ship[k]) - float(ora[k]) - abs(k[1]) * 1e-5))
        n += 1
print(f"max |residual - tail| = {worst:.2e} over {n} rows; captures {caps} agree {caps - len([k for k in dis if ora[k]=='CAPTURED'])}/{caps}")
assert dis == [], f"capture/escape flags disagree on {dis}"
assert caps == 20, f"expected the dossier's 20/20 shared captures, got {caps}"
assert worst <= 2e-9 and n == 48, "shipped-vs-oracle residual claim broken"
PYEOF
echo "== dossier numbers asserted against the regenerated record =="
python3 - <<'PYEOF'
import math, re, sys
sys.path.insert(0, '.')
import kerr_shadow2 as k

ok = True
def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    ok = ok and cond

txt = open('instrument-out.txt').read()
rows = {}
for m in re.finditer(r'(0\.\d{4})\s+([\d.]+)\s+\S+\s+\S+\s+\|\s*\[\s*(-?\d+\.\d+),\s*\+?(\d+\.\d+)\]\s*\|\s*\+-\s*(\d+\.\d+)\s*\|\s*([+-]?\d+\.\d+)/\s*([+-]?\d+\.\d+)\s*\|\s*(-?\d+\.\d+)\s*\|\s*(\d+\.\d)%\s+(\d+\.\d)%', txt):
    rows[(float(m.group(1)), float(m.group(2)))] = tuple(float(x) for x in m.groups()[2:])
check("all 21 table rows parsed", len(rows) == 21)
check("3.2M retro edges -79.62/-68.02/-65.43",
      abs(rows[(0.5, 3.2)][0] + 79.62) < .01 and abs(rows[(0.9, 3.2)][0] + 68.02) < .01
      and abs(rows[(0.998, 3.2)][0] + 65.43) < .01)
check("3.2M census 46.2/44.8/43.0 (the cap; NOT the alpha+-alpha- 40.5/32.5/29.3)",
      abs(rows[(0.5, 3.2)][7] - 46.2) < .06 and abs(rows[(0.9, 3.2)][7] - 44.8) < .06
      and abs(rows[(0.998, 3.2)][7] - 43.0) < .06)
check("pro 3.2M chi-blind errors -17.8/-34.9/-43.9",
      abs(rows[(0.5, 3.2)][3] + 17.84) < .01 and abs(rows[(0.9, 3.2)][3] + 34.85) < .01
      and abs(rows[(0.998, 3.2)][3] + 43.86) < .01)
check("retro 3.2M chi-blind errors +4.3/+15.9/+18.5 (sign flip)",
      abs(rows[(0.5, 3.2)][4] - 4.29) < .01 and abs(rows[(0.9, 3.2)][4] - 15.90) < .01
      and abs(rows[(0.998, 3.2)][4] - 18.49) < .01)
check("centre max -19.8 at (0.998,6M)", abs(rows[(0.998, 6.0)][5] + 19.84) < .01)
check("weak-chi crossings 0.183/0.435 (20M), 0.060/0.148 (6M)",
      "0.1832851" in txt and "0.4350330" in txt and "0.0599612" in txt and "0.1482831" in txt)
check("a=0 inside controls: 50.00% at 3.0M, 51.92% at 2.9M",
      "census 50.00%" in txt and "census 51.92%" in txt)
tan_ok = "retro" in txt
for line in txt.splitlines():
    if "retro" in line and "at exactly r_ph" in line:
        v = float(line.split("= ")[-1])
        tan_ok = tan_ok and abs(v - 1.0) < 1e-12
check("retro tangentiality: |sin| = 1 exactly at r_ph, all 5 spins", tan_ok)
check("pro tangential point unreachable at chi>=0.9 (inside ergosphere)",
      txt.count("INSIDE the static domain's floor") == 3)
check("edge bisection max |d sin| = 5.5e-15",
      "max |sin(flip) - sin(formula edge)| = 5.50e-15" in txt)
for a in [0.5, 0.9, 0.998]:
    rp, rm = k.photon_circular(a)
    bpc, bmc = k.bcrit(rp, a), k.bcrit(rm, a)
    ap_, am_ = k.alpha_deg(bpc, 3.2, a), k.alpha_deg(bmc, 3.2, a)
    f = (180 + ap_ - abs(am_)) / 360
    c = k.census(a, 3.2)
    check(f"cap formula == census at chi={a} ({100*f:.2f} vs {100*c:.2f})", abs(f - c) < 0.001)
print("ALL PASS" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)
PYEOF
echo "OK"
