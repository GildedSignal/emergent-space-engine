#!/bin/sh
# Regen: rebuild from work/patch.diff, refly all arms (rungs B, A', C + calibration + extension),
# recompute every dossier number. ~11 min cold (build ~3-5 min + flights ~6 min), ~7 min warm.
set -e
D=$(cd "$(dirname "$0")" && pwd)   # .../lab/results/<run>
while [ "$D" != "/" ] && [ ! -f "$D/Cargo.toml" ]; do D=$(dirname "$D"); done
cd "$D"   # repo root
R=lab/results/20261019-1817-second-20261019-1656-quant-88e9-3eb3
git apply --check $R/work/patch.diff 2>/dev/null && git apply $R/work/patch.diff || echo "patch already applied or tree carries it"
cargo build --release -p emergent-universe --example nladder
B="$CARGO_TARGET_DIR/release/examples/nladder"
[ -x "$B" ] || B=target/release/examples/nladder

# calibration: instrument match to 88e9's OFF digits (seed 1, 3e4, ~13 s)
LADDER_PROBE_GS=5000 LADDER_CAP_S=60 "$B" 30000 burn 13 2000 12 2>/dev/null | grep "probe gs" > $R/work/calib_off_seed1.log

# rung C, OFF arm: the 1e5 wall (guard 1750 as flown)
LADDER_PROBE_GS=5000 LADDER_CAP_S=400 LADDER_RSS_MB=1750 "$B" 100000 burn 55 2000 12 2>/dev/null > $R/work/a_off_100k.log
# rung A': 5e4 both arms (as registered, and as flown)
LADDER_PROBE_GS=5000 LADDER_CAP_S=300 LADDER_RSS_MB=1800 "$B" 50000 burn 55 2000 12 2>/dev/null > $R/work/ap_off_50k.log
BELT_SPLIT=1 LADDER_PROBE_GS=5000 LADDER_CAP_S=300 LADDER_RSS_MB=1800 "$B" 50000 burn 160 2000 12 2>/dev/null > $R/work/ap_on_50k.log
# extension (disclosed post-registration diagnostic): OFF 5e4 to 200k to locate onset
LADDER_PROBE_GS=5000 LADDER_CAP_S=400 LADDER_RSS_MB=1800 "$B" 50000 burn 100 2000 12 2>/dev/null > $R/work/ap_off_50k_long.log
# rung B: 3e4 seed 2, both arms, matched window [140k,245k]
LADDER_SEED=2 LADDER_PROBE_GS=5000 LADDER_CAP_S=200 LADDER_RSS_MB=1600 "$B" 30000 burn 130 2000 12 2>/dev/null > $R/work/b_off_30k_s2.log
LADDER_SEED=2 BELT_SPLIT=1 LADDER_PROBE_GS=5000 LADDER_CAP_S=200 LADDER_RSS_MB=1600 "$B" 30000 burn 140 2000 12 2>/dev/null > $R/work/b_on_30k_s2.log
# rung C, ON arm: the 1e5 wall confirmation
BELT_SPLIT=1 LADDER_PROBE_GS=5000 LADDER_CAP_S=300 LADDER_RSS_MB=1800 "$B" 100000 burn 65 2000 12 2>/dev/null > $R/work/c_on_100k.log

python3 $R/work/analysis.py 2>&1 | tee $R/work/analysis.out
echo "regen done"
