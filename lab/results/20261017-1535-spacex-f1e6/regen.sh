#!/bin/bash
# Regenerates every dossier number from shipped code + work/patch.diff (applied by the runner
# before this runs). Order matters: digests first (they are not timing-sensitive), then the
# paired A/B flights (each pair within one window; the box is shared - orders of magnitude only).
set -e
cd "$(dirname "$0")/../../.."   # repo root
T=/home/glmlab/lab-target-2/release/examples
OUT=lab/results/20261017-1535-spacex-f1e6/out
mkdir -p "$OUT"

# 1. Digest identity, the correctness proof. OFF first (must equal the frozen record
#    artifacts/runs/nladder/ladder_digests_wave.txt), then ON (must equal OFF).
timeout 500 $T/ladder_digest > "$OUT/dig_off.txt" 2>&1
ES_MEMO=1 timeout 500 $T/ladder_digest > "$OUT/dig_on.txt" 2>&1
# strip the `[x s]` wall annotations so both diffs are clean identity signals
strip() { sed -E 's/ *\[[0-9.]+ s\]$//' "$1" | grep "|" | sed 's/ *$//' | grep -v "^state:" | sort; }
diff <(strip "$OUT/dig_off.txt") <(strip "$OUT/dig_on.txt") > "$OUT/dig_diff.txt" || true
diff <(strip "$OUT/dig_off.txt") <(strip artifacts/runs/nladder/ladder_digests_wave.txt) > "$OUT/dig_record_diff.txt" || true

# 2. Paired A/B flights (each OFF run immediately before its ON run; medians of the pairs).
for spec in "10000 coast 60 600" "10000 coast 60 1800" "10000 burn 60 600" "100000 coast 55 100" "100000 coast 20 1000"; do
  tag=$(echo $spec | tr ' ' _)
  for arm in off on; do
    if [ "$arm" = on ]; then export ES_MEMO=1; else unset ES_MEMO || true; fi
    timeout 70 $T/nladder $spec > "$OUT/nladder_${tag}_${arm}.txt" 2>&1 || true
  done
done
# the repeat pair (within-window stability of the coast-600 deltas)
timeout 70 $T/nladder 10000 coast 60 600 > "$OUT/nladder_10000_coast_60_600_rep_off.txt" 2>&1 || true
ES_MEMO=1 timeout 70 $T/nladder 10000 coast 60 600 > "$OUT/nladder_10000_coast_60_600_rep_on.txt" 2>&1 || true
unset ES_MEMO || true

# 3. Summary table.
python3 - "$OUT" <<'EOF'
import re, sys, pathlib
out = pathlib.Path(sys.argv[1])
print(f"{'flight':<28} {'p50_off':>8} {'p50_on':>8} {'p99_off':>8} {'p99_on':>8} {'ev_off':>7} {'ev_on':>7} hit_rate")
for f in sorted(out.glob("nladder_*_off.txt")):
    on = f.parent / f.name.replace("_off.txt", "_on.txt")
    def parse(p):
        s = p.read_text()
        l = re.search(r"ladder: .*p50_ms=([\d.]+) p99_ms=([\d.]+) max_ms=([\d.]+) over=(\d+).*events_per_body_gs=([\d.e+-]+)", s)
        m = re.search(r"memo: hits=(\d+) misses=(\d+) entries=(\d+) hit_rate=([\d.]+)", s)
        return (float(l.group(1)), float(l.group(2)), float(l.group(3)), int(l.group(4)), l.group(5), m and float(m.group(4)))
    a, b = parse(f), parse(on)
    tag = f.stem.replace("nladder_", "").replace("_off", "")
    print(f"{tag:<28} {a[0]:>8.3f} {b[0]:>8.3f} {a[1]:>8.3f} {b[1]:>8.3f} {a[4][:7]:>7} {b[4][:7]:>7} {b[5]}")
EOF
echo "regen done"
