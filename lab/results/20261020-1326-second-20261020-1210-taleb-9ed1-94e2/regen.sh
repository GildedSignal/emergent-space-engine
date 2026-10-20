#!/usr/bin/env bash
# Regen: rebuild the patched example (work/patch.diff is applied by the runner before this runs),
# re-fly the six arms, reprint every dossier number. ~11 min on 8 vCPU, single flights (no load added).
# Private target dir (work/target): the shared lab-target-2 is clobbered by this window's other runs
# (measured: a foreign nladder replaced ours mid-run on 20 Oct; md5 differs after ~10 min).
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root
ROOT="$(pwd)"
RUN="$ROOT/lab/results/20261020-1326-second-20261020-1210-taleb-9ed1-94e2"
W="$RUN/work"
export CARGO_TARGET_DIR="$W/target"

# 0. patch expected applied by the runner; apply if not.
if ! grep -q ans_chunking crates/universe/src/encounter.rs; then git apply "$W/patch.diff"; fi
cargo build --release -p emergent-universe --example nladder 2>&1 | tail -1
BIN="$W/target/release/examples/nladder"

fly () {  # fly <csv> <N> <sec> <trace 0|1> <chunk 0|1> [maxwall]
  local out=$1 n=$2 sec=$3 trace=$4 chunk=$5 mw=${6:-240}
  local args=""
  [ "$trace" = 1 ] && args="ES_ANS_TRACE=1"
  [ "$chunk" = 1 ] && args="$args ES_ANS_CHUNK=1"
  env ES_FRAME_CSV=1 ES_SCAN_TTL_S=16 ES_STAGGER_GS=14000 $args ES_MAX_WALL_S=$mw \
      "$BIN" "$n" burn "$sec" 400 12 1 > "$W/$out" 2> "$W/${out%.csv}.err"
  grep "^ladder:" "$W/$out" | sed "s/^/$(basename "$out" .csv) /"
}

fly T1_1e5.csv 100000 130 1 0 200   # T1 the answer path at the birth rung
fly T2_2e5.csv 200000 130 1 0 240   # T2 ditto at 2e5
fly T3_3e5.csv 300000 120 1 0 300   # T3 the freeze object, instrumented
fly C3_3e5.csv 300000 120 1 1 300   # C3 the fix: incremental answering at the frame budget
fly C1_1e5.csv 100000 130 1 1 200   # C1 the fix at the birth rung

python3 "$W/analyze94.py" "$W/T1_1e5.csv" "$W/T1_1e5.err" "T1 1e5 fence/stag14k trace"
python3 "$W/analyze94.py" "$W/T2_2e5.csv" "$W/T2_2e5.err" "T2 2e5 fence/stag14k trace"
python3 "$W/analyze94.py" "$W/T3_3e5.csv" "$W/T3_3e5.err" "T3 3e5 fence/stag14k trace"
python3 "$W/analyze94.py" "$W/C3_3e5.csv" "$W/C3_3e5.err" "C3 3e5 chunk"
python3 "$W/analyze94.py" "$W/C1_1e5.csv" "$W/C1_1e5.err" "C1 1e5 chunk"
# the freeze object's own line, and the en-object comparison across arms
for f in T3_3e5 C3_3e5; do
  echo "-- $f biggest answers:"; grep esans "$W/$f.err" | awk -F'ns=' '{split($2,a," "); if (a[1]+0>50000000) print}' | cut -c1-140
done
python3 - "$W" <<'EOF'
import sys
sys.path.insert(0, sys.argv[1])
from analyze94 import load_ans, frames
w = sys.argv[1]
for arm in ["T1_1e5", "T2_2e5", "T3_3e5", "C3_3e5", "C1_1e5"]:
    fr = frames(f"{w}/{arm}.csv")
    enb = [r for r in fr if r["en"] > 0]
    print(f"{arm}: frames en>0 {len(enb)}, max en {max((r['en'] for r in enb), default=0)}, "
          f"sum en {sum(r['en'] for r in enb)}, max_ms {max(r['ms'] for r in fr):.1f}, "
          f"over12 {sum(1 for r in fr if r['ms'] > 12)}, rss {max(r['rss'] for r in fr):.0f} MB, "
          f"held {max(r['held'] for r in fr)}")
EOF
echo "regen done"
