#!/bin/sh
# Regen (from a clean checkout): apply the run's patch, build, re-fly the dossier's arms.
# The numbers regenerate in ~4 min on the lab box (flights are 30-90 s each).
set -e
cd "$(dirname "$0")/../../.." # repo root
git apply lab/results/20261019-1452-library-e181/work/patch.diff || echo "patch already applied"
cargo build --release -p emergent-universe --example nladder
BIN=$CARGO_TARGET_DIR/release/examples/nladder
[ -x "$BIN" ] || BIN=target/release/examples/nladder
OUT=lab/results/20261019-1452-library-e181/work/logs
mkdir -p $OUT
# The instrument's negative control (coast holds <=1, the record's bpb/catalogue digits):
$BIN 10000 coast 20 100 12 > $OUT/ctrl_10e4_coast.log 2>&1
# Arm A, shipped (the ratchet): guard 1,600 MB at ~29.6k game-s.
LADDER_CAP_S=420 LADDER_RSS_MB=1600 LADDER_PROBE_GS=1000 $BIN 100000 burn 420 100 12 > $OUT/A2_shipped.log 2>&1
# Arm B, the fence (TTL 16 game-s): no guard, flat ~650-700 MB, 41.9k game-s.
LADDER_CAP_S=420 LADDER_RSS_MB=1600 LADDER_PROBE_GS=1000 ES_SCAN_TTL_S=16 $BIN 100000 burn 420 100 12 > $OUT/B2_ttl16.log 2>&1
# Arm C, TTL 8 (the fence scales): flat 642 MB at 24k game-s.
LADDER_CAP_S=240 LADDER_RSS_MB=1600 LADDER_PROBE_GS=1000 ES_SCAN_TTL_S=8 $BIN 100000 burn 240 100 12 > $OUT/C_ttl8.log 2>&1
echo "== headline numbers =="
for f in ctrl_10e4_coast A2_shipped B2_ttl16 C_ttl8; do
  echo "-- $f"; grep -E "guard:|^game .*stats|^ladder:|^scans:" $OUT/$f.log
done
