#!/bin/sh
# Regen: rebuild the patched nladder example, fly the five arms, reprint the dossier's
# table and derived ledger from the ladder: lines. Runs ~4 min on 8 vCPU (build ~60 s
# from a warm deps cache, flights ~135 s). Patch (work/patch.diff) is applied by the
# runner before this runs; if not, apply it here.
set -e
cd "$(dirname "$0")/../../.."
if ! grep -q 'not(target_os = "macos")' crates/universe/examples/nladder.rs 2>/dev/null; then
  git apply "$OLDPWD/work/patch.diff" 2>/dev/null || git apply "${0%/*}/work/patch.diff"
fi
cargo build --release -p emergent-universe --example nladder 2>&1 | tail -1
B=$(ls -1 target/release/examples/nladder 2>/dev/null || true)
[ -x "$B" ] || B=/home/glmlab/lab-target-3/release/examples/nladder
OUT="${0%/*}/flights.log"
: > "$OUT"
for args in "100000 coast 20 100" "100000 coast 20 600" "300000 coast 20 100" "300000 coast 20 600" "300000 coast 20 1800"; do
  "$B" $args >> "$OUT" 2>&1 || echo "FAILED $args" >> "$OUT"
done
python3 - "${0%/*}" <<'EOF'
import re, sys
rows = {}
for line in open(sys.argv[1] + "/flights.log"):
    m = re.match(r"ladder: n=(\d+).*rtf=(\d+).*frames=(\d+).*p50_ms=([\d.]+) p99_ms=([\d.]+).*lag_s=([\d.]+) kicks_per_body_gs=([\d.e-]+) events_per_body_gs=([\d.e-]+)", line)
    if m:
        n, rtf = int(m[1]), int(m[2])
        rows[(n, rtf)] = dict(frames=int(m[3]), p50=float(m[4]), p99=float(m[5]), lag=float(m[6]),
                              kicks=float(m[7]), events=float(m[8]))
# absolute counts come from the prose lines (kicks/events totals)
totals = {}
for line in open(sys.argv[1] + "/flights.log"):
    m = re.match(r"rung N=(\d+) \(\d+ bodies\), coast, rtf (\d+).*", line)
    if m:
        cur = (int(m[1]), int(m[2]))
    m = re.match(r"game ([\d.]+) s after the first second: kicks (\d+) .* events (\d+) ", line)
    if m and cur:
        totals[cur] = (float(m.group(1)), int(m.group(2)), int(m.group(3)))
for (n, rtf), (gs, k, e) in sorted(totals.items()):
    r = rows.get((n, rtf), {})
    print(f"N={n:>7} rtf={rtf:>4} game-s={gs:>8.0f} kicks={k:>7} events={e:>7} p50ms={r.get('p50',0):>7.3f} lag={r.get('lag',0):>6.2f}s")
# anchors + ledger
import statistics
costs = []
if (300000, 1800) in rows and (100000, 600) in rows:
    c1 = rows[(300000,1800)]["p50"]*1e3/235          # clamped frame: 235 events p50
    c2 = rows[(100000,600)]["p50"]*1e3/23
    costs = [c1, c2]
C = statistics.median(costs) if costs else 50.0
print(f"\ncost anchor ~{C:.1f} us/event (p50 ms / p50 events, two arms)")
R = 1/28141.5                                       # doll-grid interval, 3294/cf45
for rtf in (1, 10, 100):
    print(f"10^9 quiet-belt kick rail @ rtf {rtf:>3}: {1e9*R*rtf*C*1e-6:7.1f} cores (average)")
for N in (3e5, 1e6, 1e9):
    print(f"freeze at N={N:.0e}: {N*C*1e-6/0.72/3600:8.2f} h per crest (one budget-core)")
print(f"clock gap own-period vs doll grid: {R/(64/3.15e7):.0f}x at 1 AU, {R/(64/8.9e7):.0f}x at 2 AU")
print(f"measured B3 lag {rows.get((300000,1800),{}).get('lag',0):.1f} s vs predicted {3e5*C*1e-6/0.72:.1f} s")
EOF
