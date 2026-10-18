#!/bin/sh
# Regenerates every number in dossier.md from a restored tree: applies work/patch.diff
# (7581's harness verbatim, deduplicated: 604c formation + f134 arms + scan census/prof),
# builds scanprobe, flies the control, the K-trend, the decisive arm and the OFF contrast.
# Deterministic columns (kicks/events/game_s/digest/scan census) must match exactly;
# wall columns (ms, us/frame) are shared-box orders of magnitude. ~4 min cold.
set -e
cd "$(dirname "$0")/../../.."   # repo root
P="$(dirname "$0")/work/patch.diff"
if git apply --check --reverse "$P" 2>/dev/null; then
  echo "patch already applied; skipping"
elif git apply --check "$P" 2>/dev/null; then
  git apply "$P"
else
  git apply --3way "$P" || { echo "patch does not apply to this tree" >&2; exit 1; }
fi
cargo build --release --features prof -p emergent-universe --example scanprobe
B=${CARGO_TARGET_DIR:-target}/release/examples/scanprobe
OUT="$(dirname "$0")/regen"; mkdir -p "$OUT"; cd "$OUT"
# arming control + K-trend + decisive + OFF contrast (composed = ES_SECULAR+ES_CHAIN+ES_LOCAL_STAGGER)
env ES_SECULAR=1 ES_CHAIN=1 ES_LOCAL_STAGGER=1 $B 10000 0 10 100 > comp-10000.log 2>&1
env ES_SECULAR=1 ES_CHAIN=1 ES_LOCAL_STAGGER=1 $B 20000 0 10 100 > comp-20000.log 2>&1
env ES_SECULAR=1 ES_CHAIN=1 ES_LOCAL_STAGGER=1 $B 30000 0 10 100 > comp-30000.log 2>&1
rm -f dump-comp-50k.txt
env ES_SECULAR=1 ES_CHAIN=1 ES_LOCAL_STAGGER=1 ES_DUMP=dump-comp-50k.txt $B 50000 0 10 100 > comp-50000.log 2>&1
env $B 50000 0 10 100 > off-50000.log 2>&1
for f in comp-10000 comp-20000 comp-30000 comp-50000 off-50000; do
  echo "== $f"; grep -E "^(probe|comb|scan):" $f.log; grep "capture (cheap" $f.log
done
echo "== over-frame attribution (dump-comp-50k.txt)"
python3 - <<'EOF'
rows=[tuple(map(float,l.split())) for l in open("dump-comp-50k.txt")]
late=[r for r in rows if r[0]>=60]
over=[r for r in late if r[1]>12.0]
ev=sorted(r[2] for r in over)
print(f"late={len(late)} over={len(over)} over-events-median={ev[len(ev)//2]:.0f} max={ev[-1]:.0f} over-ms-mean={sum(r[1] for r in over)/max(1,len(over)):.2f} frames-ev>40={sum(1 for r in late if r[2]>40)}")
EOF
echo "regen done: deterministic columns must equal dossier tables; comb max_ev at 5e4 may slide 28<->29 across executions (deadline-coupled, disclosed)"
