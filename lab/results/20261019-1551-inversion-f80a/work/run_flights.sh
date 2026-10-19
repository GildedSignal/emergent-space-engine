#!/bin/sh
# The run's flights (20261019-1551-inversion-f80a). Binary: e181's patch verbatim
# + frame-loop prune() RESTORED (its checker's correction (a)) + history_census probe.
# Scene: nladder 3x10^4 seed 1, L8 burn from frame 60, rtf 1000, 12 ms budget,
# probe every 1,000 game-s, RSS guard 1,600 MB (box cap 2 GB).
# rtf 1000 reaches channel 2's onset (~95-130k game-s) inside the window; the
# memory laws (mints/game-s, TTL in game-s, keep windows) are rtf-invariant.
set -e
cd "$(dirname "$0")/../../../.." # repo root
BIN=${CARGO_TARGET_DIR:-target}/release/examples/nladder
OUT=lab/results/20261019-1551-inversion-f80a/work/logs
mkdir -p $OUT
# Arm OFF: shipped behaviour (TTL unset, prune restored) - channel 2 onset control.
LADDER_CAP_S=175 LADDER_RSS_MB=1600 LADDER_PROBE_GS=1000 $BIN 30000 burn 175 1000 12 > $OUT/off_pruned.log 2>&1 || true
# Arm ON: the fence (TTL 16 game-s), prune restored - the decisive arm past onset.
LADDER_CAP_S=420 LADDER_RSS_MB=1600 LADDER_PROBE_GS=1000 ES_SCAN_TTL_S=16 $BIN 30000 burn 420 1000 12 > $OUT/on_ttl16.log 2>&1 || true
echo done
