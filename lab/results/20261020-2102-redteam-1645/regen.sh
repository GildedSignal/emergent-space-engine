#!/bin/sh
# Regen for 20261020-2102-redteam-1645. The runner applies work/patch.diff
# (adds crates/space/tests/kerr_view_probe.rs) before this runs.
# Total: ~15 s (python) + ~5 s (cargo, warm; first build may take minutes).
set -e
cd "$(dirname "$0")"
python3 kerr_shadow.py > instrument-out.txt
( cd ../../../crates/space && \
  cargo test -p emergent-space --test kerr_view_probe -- --nocapture 2>/dev/null \
  | grep -E "^DEFL" ) > shipped-defl.txt
echo "== shipped vs oracle residual (expect exactly |b|e-5 = 2b/r_max tail) =="
python3 - <<'EOF'
import re
ora = {}
for line in open('instrument-out.txt'):
    m = re.match(r'ORACLE a=([\d.]+) b=([+-][\d.]+) phi=([\d.]+|CAPTURED)', line)
    if m:
        ora[(float(m.group(1)), float(m.group(2)))] = m.group(3)
worst = 0.0
for line in open('shipped-defl.txt'):
    m = re.match(r'DEFL a=([\d.]+) b=([+-][\d.]+) (?:phi=([\d.]+)|CAPTURED)', line)
    if not m or m.group(3) is None:
        continue
    a, b, phi = float(m.group(1)), float(m.group(2)), float(m.group(3))
    o = ora.get((a, b))
    if o:
        res = phi - float(o)
        worst = max(worst, abs(res - abs(b) * 1e-5))
        print(f"a={a} b={b:+.4f} shipped {phi:.9f} oracle {o} residual {res:+.2e} "
              f"(tail |b|e-5 = {abs(b)*1e-5:.2e})")
print(f"max |residual - tail| = {worst:.2e}  (0 => shipped matches oracle to printed digits)")
EOF
echo "OK"
