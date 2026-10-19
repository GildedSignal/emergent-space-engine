#!/bin/sh
# Regen: rebuild from work/patch.diff, fly both arms, recompute the slopes. ~5 min.
set -e
D=$(cd "$(dirname "$0")" && pwd)   # .../lab/results/<run>
while [ "$D" != "/" ] && [ ! -f "$D/Cargo.toml" ]; do D=$(dirname "$D"); done
cd "$D"   # repo root (the checkout with Cargo.toml)
git apply --check lab/results/20261019-1656-quant-88e9/work/patch.diff 2>/dev/null && git apply lab/results/20261019-1656-quant-88e9/work/patch.diff || echo "patch already applied or tree carries it"
cargo build --release -p emergent-universe --example nladder
B="$CARGO_TARGET_DIR/release/examples/nladder"
[ -x "$B" ] || B=target/release/examples/nladder
R=lab/results/20261019-1656-quant-88e9
LADDER_PROBE_GS=5000 LADDER_CAP_S=200 LADDER_RSS_MB=1600 "$B" 30000 burn 130 2000 12 > $R/work/off_200k.log 2>/dev/null
BELT_SPLIT=1 LADDER_PROBE_GS=5000 LADDER_CAP_S=210 LADDER_RSS_MB=1600 "$B" 30000 burn 140 2000 12 > $R/work/on_260k.log 2>/dev/null
python3 $R/work/slopes.py
