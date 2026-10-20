#!/usr/bin/env bash
# Regen: rebuild the patched example (work/patch.diff is applied by the runner before this runs),
# re-fly all 11 arms fresh, reprint every dossier number from the CSVs. ~12 min on 8 vCPU.
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root
ROOT="$(pwd)"
RUN="$ROOT/lab/results/20261020-1210-taleb-9ed1"
W="$RUN/work"
BIN=/home/glmlab/lab-target-2/release/examples/nladder
export CARGO_TARGET_DIR=/home/glmlab/lab-target-2

# 0. patch expected applied by the runner; apply if not.
if ! grep -q birth_stagger_ticks crates/universe/src/step.rs; then git apply "$W/patch.diff"; fi
cargo build --release -p emergent-universe --example nladder 2>&1 | tail -1

fly () {  # fly <csv> <N> <sec> <seed> <ttl> <stag> [maxwall]
  local out=$1 n=$2 sec=$3 seed=$4 ttl=$5 stag=$6 mw=${7:-240}
  env ES_FRAME_CSV=1 ES_SCAN_TTL_S=$ttl ES_STAGGER_GS=$stag ES_MAX_WALL_S=$mw \
      "$BIN" "$n" burn "$sec" 400 12 "$seed" > "$W/$out" 2>&1
  grep "^ladder:" "$W/$out" | sed "s/^/$(basename $out .csv) /"
}
# anchor (fence off) then the arms, exactly as flown (predictions.md table)
fly a0_anchor_1e5.csv 100000 150 1 0 0      200   # A0 anchor, fence off
fly A1_1e5.csv         100000 150 1 16 0    200   # A1
fly A2_1e5.csv         100000 150 1 16 14000 200  # A2
fly A3_2e5.csv         200000 130 1 16 0    240   # A3
fly A4_2e5.csv         200000 130 1 16 14000 240  # A4
fly A5.csv             300000 120 1 16 0    300   # A5
fly A6.csv             300000 120 1 16 14000 300  # A6
fly A7.csv             200000 130 2 16 14000 240  # A7
fly A9_stag_8era.csv   100000 300 1 16 14000 300  # A9
fly A11_ttl8_3e5.csv   300000 120 1 8  14000 300  # A11

# A8 under load-16 (busy loops), killed after the flight
for i in $(seq 1 16); do timeout 130 bash -c 'while :; do :; done' & done > /dev/null 2>&1
sleep 1
fly A8_load16_1e5.csv  100000 150 1 16 14000 200   # A8
pkill -f 'while :; do :; done' 2>/dev/null || true

cd "$W"
python3 analyze.py a0_anchor_1e5.csv "A0 1e5 off/off"
python3 analyze.py A1_1e5.csv "A1 1e5 fence/off"
python3 analyze.py A2_1e5.csv "A2 1e5 fence/stag14k"
python3 analyze.py A3_2e5.csv "A3 2e5 fence/off"
python3 analyze.py A4_2e5.csv "A4 2e5 fence/stag14k"
python3 analyze.py A5.csv "A5 3e5 fence/off"
python3 analyze.py A6.csv "A6 3e5 fence/stag14k"
python3 analyze.py A7.csv "A7 2e5 fence/stag14k seed2"
python3 analyze.py A8_load16_1e5.csv "A8 1e5 fence/stag14k load16"
python3 analyze.py A9_stag_8era.csv "A9 1e5 fence/stag14k 8 eras"
python3 analyze.py A11_ttl8_3e5.csv "A11 3e5 ttl8/stag14k"
# worst-frame payloads (the en=178 answer frame and its peers) and A9 persistence bins
python3 - <<'EOF'
from analyze import load, KICK_ERAS
for name in ["A2_1e5.csv","A4_2e5.csv","A7.csv","A6.csv","A3_2e5.csv","A5.csv","A11_ttl8_3e5.csv","A8_load16_1e5.csv"]:
    for r in sorted(load(name), key=lambda r: -r["ms"])[:3]:
        print(f"{name}: f{r['f']} {r['ms']:8.1f}ms ev{r['ev']:>6} k{r['k']:>6} en{r['en']:>4} held{r['held']} gs{r['gs']:.0f}")
rows = load("A9_stag_8era.csv")
for lo, hi in KICK_ERAS:
    sel = [r for r in rows if lo <= r["gs"] < hi]
    if not sel: continue
    plo, phi = lo - 14000, hi
    full = sum(r["k"] for r in rows if plo <= r["gs"] < phi)
    bins = {}
    for r in rows:
        if plo <= r["gs"] < phi:
            b = int(r["gs"] // 1000); bins[b] = bins.get(b, 0) + r["k"]
    hf = max(bins.items(), key=lambda kv: kv[1])
    print(f"A9 kick era [{lo//1000},{hi//1000})k: full-span kicks {full}, hot bin {100*hf[1]/full:.1f}%")
EOF
echo "regen done"
