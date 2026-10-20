#!/usr/bin/env bash
# Regen: rebuild the patched nladder (work/patch.diff applied by the runner before this runs),
# re-fly the anchor and all four arms fresh (no [ -s ] reuse guards), re-run the decomposition.
# ~4 min warm: build ~10 s, anchor 20 s, four flights 33-46 s each, analysis < 1 min.
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root
ROOT="$(pwd)"
RUN="$ROOT/lab/results/20261020-1116-second-20261020-1002-inversion-0a46-8365"
W="$RUN/work"
BIN=/home/glmlab/lab-target-2/release/examples/nladder

# 0. the patch is expected already applied (the runner applies work/patch.diff); if not, apply it.
if ! grep -q birth_stagger_ticks crates/universe/src/step.rs; then git apply "$W/patch.diff"; fi
export CARGO_TARGET_DIR=/home/glmlab/lab-target-2
cargo build --release -p emergent-universe --example nladder 2>&1 | tail -1

# 1. anchor: CSV off, stagger off — must land in the record's shipanchor family (max 780-960 ms at 1e5 rtf 2000)
"$BIN" 100000 burn 10 2000 12 1 | grep "ladder:" | tee "$W/anchor.txt"

# 2. the four arms, re-flown fresh every time (decisive flights)
cd "$W"
ES_FRAME_CSV=1 "$BIN" 100000 burn  150 400 12 1 > m1_burn_1e5.csv 2>&1
ES_FRAME_CSV=1 "$BIN" 100000 coast 150 400 12 1 > m2_coast_1e5.csv 2>&1
ES_FRAME_CSV=1 ES_STAGGER_GS=4000  "$BIN" 100000 burn 150 400 12 1 > s1_stag4k_burn.csv 2>&1
ES_FRAME_CSV=1 ES_STAGGER_GS=14000 "$BIN" 100000 burn 150 400 12 1 > s2_stag14k_burn.csv 2>&1

# 3. the era/payload decomposition (every dossier table regenerates here)
python3 eras2.py m1_burn_1e5.csv   100028 "M1 1e5 burn"
python3 eras2.py m2_coast_1e5.csv  100028 "M2 1e5 coast"
python3 eras2.py s1_stag4k_burn.csv 100028 "S1 1e5 burn stagger 4k"
python3 eras2.py s2_stag14k_burn.csv 100028 "S2 1e5 burn stagger 14k"
# the payload split per era (kicks vs boundaries) for M1/M2, as the dossier quotes it
python3 - <<'EOF'
from eras2 import load
for name in ["m1_burn_1e5.csv", "m2_coast_1e5.csv"]:
    rows = load(name); print("==", name)
    for lo, hi, lab in [(12000,16000,"era1"),(26000,30000,"era2"),(40000,44000,"era3"),(54000,58000,"era4")]:
        sel = [r for r in rows if lo <= r["gs"] < hi]
        k=sum(r["k"] for r in sel); bo=sum(r["bo"] for r in sel); ev=sum(r["ev"] for r in sel)
        it2=sum(r["it"][2] for r in sel); it3=sum(r["it"][3] for r in sel)
        cn2=sum(r["cn"][2] for r in sel)/1e3; cn3=sum(r["cn"][3] for r in sel)/1e3
        w=sum(r["ms"] for r in sel)/1e3
        print(f"{lab}: ev {ev} kicks {k} boundaries {bo} it2 {it2} it3 {it3} wall {w:.1f}s cn2 {cn2:.2f}s cn3 {cn3:.2f}s")
EOF
echo "regen done"
