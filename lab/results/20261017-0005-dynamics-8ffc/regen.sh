#!/bin/sh
# Regen: rebuild the patched nladder (work/patch.diff: print-only — 9e75's Linux footprint,
# the per-spell crest table, the ES_TRACE per-frame trace, the wall cap raised; no law, no
# schedule), fly the three arms sequentially (timing arms must not contend), and reprint the
# crest table + the delivery-independent comb masses. ~4 min warm on 8 vCPU; peak RSS 1.45 GB.
set -e
cd "$(dirname "$0")/../../.."
R="${0%/*}"
if ! grep -q 'spell: count=' crates/universe/examples/nladder.rs 2>/dev/null; then
  git apply "$R/work/patch.diff"
fi
if [ -d /home/glmlab/lab-target-8ffc ]; then
  export CARGO_TARGET_DIR=/home/glmlab/lab-target-8ffc
fi
cargo build --release -p emergent-universe --example nladder 2>&1 | tail -1
B="$CARGO_TARGET_DIR/release/examples/nladder"
[ -x "$B" ] || B=target/release/examples/nladder
{ date; uptime; free -m | head -2; } > "$R/work/state-a.txt"
: > "$R/work/flights.log"
i=0
for args in "300000 coast 150 1800" "100000 coast 60 3600" "300000 coast 100 300"; do
  i=$((i + 1)); case $i in 1) a=A;; 2) a=B;; 3) a=C;; esac
  echo "=== arm$a: $args" | tee -a "$R/work/flights.log"
  ES_TRACE=1 "$B" $args > "$R/work/arm$a.log" 2>&1 || echo "FAILED $args" | tee -a "$R/work/flights.log"
done
{ date; uptime; } >> "$R/work/state-a.txt"
# the crest table (spell-based) per arm
python3 - "$R" <<'EOF' | tee "$R/crest.txt"
import sys, os
R = sys.argv[1]
sys.path.insert(0, R)
os.chdir(R)
import crest
for a in ("A", "B", "C"):
    p = f"work/arm{a}.log"
    if os.path.exists(p):
        spells, trace, hdr = crest.parse(p)
        crest.report(p, spells, trace, hdr)
EOF
# the comb masses (game-time windows, rtf-free)
python3 - "$R" <<'EOF' | tee "$R/combs.txt"
import sys
R = sys.argv[1]
def load(p):
    tr = []
    for line in open(p):
        if line.startswith('t: '):
            f, ms, ev, k, b, pres, df = line[3:].strip().split(',')
            tr.append((int(f), float(ms), int(ev), int(k), int(b), float(pres), float(df)))
    return tr
for arm, path, N in (('A 3e5 rtf1800', f'{R}/work/armA.log', 300000), ('B 1e5 rtf3600', f'{R}/work/armB.log', 100000), ('C 3e5 rtf300', f'{R}/work/armC.log', 300000)):
    tr = load(path)
    print(f"=== {arm} (N={N})")
    for i in range(4):
        lo, hi = 11800 + i * 28141.5, 18500 + i * 28141.5
        w = [t for t in tr if lo <= t[5] <= hi]
        if w:
            kk, bb = sum(t[3] for t in w), sum(t[4] for t in w)
            print(f"  kick window {i+1} [{lo:>6.0f},{hi:>6.0f}]: kicks {kk:>7d} ({kk/N:.3f}/body)  bnd {bb:>6d}")
    for i in range(3):
        lo, hi = 25500 + i * 28141.5, 32500 + i * 28141.5
        w = [t for t in tr if lo <= t[5] <= hi]
        if w:
            kk, bb = sum(t[3] for t in w), sum(t[4] for t in w)
            print(f"  bnd  window {i+1} [{lo:>6.0f},{hi:>6.0f}]: bnd {bb:>7d} ({bb/N:.3f}/body)  kicks {kk:>6d}")
    w = [t for t in tr if 19000 <= t[5] <= 25000]
    if w:
        span = w[-1][5] - w[0][5]
        print(f"  gap [19k,25k]: events {sum(t[2] for t in w)} over {span:.0f} game-s = {sum(t[2] for t in w)/span:.2f} ev/game-s")
EOF
echo "regen done"
