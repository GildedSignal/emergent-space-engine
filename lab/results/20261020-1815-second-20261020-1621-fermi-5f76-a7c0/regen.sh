#!/bin/sh
# Regenerates every dossier number from the clean tree.
#   patch.diff  = 8994/5f76's instrument (env-gated scope marker + counting GlobalAlloc)
#                 + this run's additions (ES_BT backtrace census, VmHWM peak-rss print).
#   withcap.diff = the measured deletion: with_capacity at the two named sites
#                 (encounter.rs candidates, radial.rs ids) — allocation-pattern only.
# Arms: BT (name the sites), C1 control, D1 deletion, S1 saturation (K=6e5, the nearest
# feasible decade to the checker's 10^6: at the shipped ~2.35 KB/body build a 10^6 flight
# is a ~2.35 GB process, over this box's 2 GB ceiling; 6e5 peaks at ~1.92 GB).
# ~4-5 min warm (two partial rebuilds + 4 flights: 21+12+12+48 s); every process < 2 GB.
set -e
D=$(dirname "$0")
while [ "$D" != / ] && [ ! -f "$D/Cargo.toml" ]; do D=$D/..; done
cd "$D" || exit 1
[ -f Cargo.toml ] || { echo "FATAL: repo root not found" >&2; exit 1; }
R=lab/results/20261020-1815-second-20261020-1621-fermi-5f76-a7c0
mkdir -p /tmp/second
BUILDD() { cargo build --release -p emergent-universe --example alloc_scope 2>&1 | tail -1; }
B=$(cargo metadata --format-version 1 --no-deps 2>/dev/null | tr ',' '\n' | grep -o '"target_directory":"[^"]*"' | cut -d'"' -f4)/release/examples

# 1. instrument on
if git apply --check "$R/work/patch.diff" 2>/dev/null; then
  git apply "$R/work/patch.diff"
elif [ -f crates/universe/examples/alloc_scope.rs ]; then
  echo "instrument patch already applied; continuing"
else
  echo "FATAL: instrument patch neither applies nor is applied" >&2; exit 1
fi
BUILDD
# BT: the naming arm (samples backtraces of player-scope >=2KiB calls; stderr carries one raw stack)
ES_ALLOC_SCOPE=1 ES_BT=1 "$B/alloc_scope" 10000 coast 30 2000 12 > /tmp/second/BT.log 2>&1
# C1: control (must reproduce 5f76's A1: player 193.4 KB/item, realloc share ~80%)
ES_ALLOC_SCOPE=1 ES_ALLOC_CSV=/tmp/second/C1.csv "$B/alloc_scope" 10000 coast 30 2000 12 > /tmp/second/C1.log 2>&1
# S1: saturation arm at the top of the flyable range (peak RSS ~1.92 GB, under the 2 GB rule)
ES_ALLOC_SCOPE=1 ES_SEED=2 ES_ALLOC_CSV=/tmp/second/S1.csv "$B/alloc_scope" 600000 coast 30 2000 12 > /tmp/second/S1.log 2>&1

# 2. the deletion on top of the instrument
if git apply --check "$R/work/withcap.diff" 2>/dev/null; then
  git apply "$R/work/withcap.diff"
elif grep -q with_capacity crates/universe/src/encounter.rs; then
  echo "withcap patch already applied; continuing"
else
  echo "FATAL: withcap patch neither applies nor is applied" >&2; exit 1
fi
BUILDD
# D1: the measured deletion (same flight as C1)
ES_ALLOC_SCOPE=1 ES_ALLOC_CSV=/tmp/second/D1.csv "$B/alloc_scope" 10000 coast 30 2000 12 > /tmp/second/D1.log 2>&1
# canonical neutrality: the engine's own suite with the deletion applied (all must pass)
cargo test -p emergent-universe --release --lib --tests 2>&1 | grep -E "test result" | tee /tmp/second/tests.log
git checkout -- crates/universe/src/encounter.rs crates/universe/src/radial.rs

echo "=== arms flown; analysis (grep the BT site census in BT.log):"
python3 "$R/analyze.py" /tmp/second
echo "=== compare with dossier.md's table (C1/D1/S1 rows) and BT.log's site census"
