#!/bin/sh
# b911: regenerate every dossier number from shipped code + work/patch.diff.
# Patch applied by the runner before this runs. ~6 min on the lab box.
set -e
cd "$(dirname "$0")/../../.."   # repo root
RUN=lab/results/20261019-1551-second-20261019-1452-taleb-527a-b911
mkdir -p $RUN/work/logs
cargo build --release -p emergent-universe --example nladder
BIN=${CARGO_TARGET_DIR:-target}/release/examples/nladder
L=$RUN/work/logs

# A: live to the RSS guard (the regression series and the guard-window split)
ES_PROBE_EVERY_GS=2000 ES_WALL_CAP_S=700 LADDER_RSS_MB=1600 $BIN 30000 burn 7200 100 12 > $L/live-guard.log 2>&1
# B: freeze both retention terms at 30k gs
ES_FREEZE_LD_AT_GS=30000 ES_PROBE_EVERY_GS=1000 ES_WALL_CAP_S=400 LADDER_RSS_MB=1600 $BIN 30000 burn 1800 100 12 > $L/freeze-30k.log 2>&1
# C: freeze both retention terms at 60k gs
ES_FREEZE_LD_AT_GS=60000 ES_PROBE_EVERY_GS=1000 ES_WALL_CAP_S=500 LADDER_RSS_MB=1600 $BIN 30000 burn 2400 100 12 > $L/freeze-60k.log 2>&1
# D/E: the term-split bisect at 30k gs (key only / keep only)
ES_FREEZE_LD_AT_GS=30000 ES_FREEZE_LD_WHERE=key ES_PROBE_EVERY_GS=2000 ES_WALL_CAP_S=500 LADDER_RSS_MB=1600 $BIN 30000 burn 1700 100 12 > $L/freeze-30k-key.log 2>&1
ES_FREEZE_LD_AT_GS=30000 ES_FREEZE_LD_WHERE=keep ES_PROBE_EVERY_GS=2000 ES_WALL_CAP_S=500 LADDER_RSS_MB=1600 $BIN 30000 burn 1700 100 12 > $L/freeze-30k-keep.log 2>&1

python3 $RUN/work/analyze.py $L/live-guard.log $L/freeze-30k.log $L/freeze-60k.log $L/freeze-30k-key.log $L/freeze-30k-keep.log
