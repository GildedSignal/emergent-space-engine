#!/bin/bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff.
# ~11 min of flights on this 8-vCPU box after a ~3 min cold build (warm: ~15 s).
# The tree patch (quant-1d52's seam+retention + b0ed's bounded rule ES_RETAIN_MAX +
# this run's instrumentation ES_MINT_WHO / admission rule ES_RETAIN_ONCE) is applied
# by the runner before this runs; if the tree is clean instead, apply it here.
set -euo pipefail
cd "$(dirname "$0")"
RUNDIR=$(pwd)
ROOT=$(git rev-parse --show-toplevel)
if ! grep -q "retain_bound_counters" "$ROOT/crates/universe/src/bind.rs" 2>/dev/null; then
  git -C "$ROOT" apply "$RUNDIR/work/patch.diff"
fi

# Private target dir: a sibling checkout must not swap the binary mid-run (0757's lesson).
export CARGO_TARGET_DIR="${RUNDIR}/target-private"
cd "$ROOT/crates/universe"
cargo build --release --example lazy_flight
BIN="$CARGO_TARGET_DIR/release/examples/lazy_flight"
[ -x "$BIN" ]

cd "$RUNDIR"

# 1. Coast anchor (patch fidelity: must reproduce b0ed's table bit-for-bit).
for a in "ctl env -u" ; do :; done
env -u ES_LAZY_ENTRY -u ES_RETAIN -u ES_RETAIN_MAX -u ES_MINT_WHO -u ES_RETAIN_ONCE "$BIN" 10000 coast 20000 1 > flights/ctl_10000_coast_20000_1.txt 2>&1
env -u ES_RETAIN_MAX -u ES_MINT_WHO -u ES_RETAIN_ONCE ES_LAZY_ENTRY=1 ES_RETAIN=1 "$BIN" 10000 coast 20000 1 > flights/retain_10000_coast_20000_1.txt 2>&1
env -u ES_MINT_WHO -u ES_RETAIN_ONCE ES_LAZY_ENTRY=1 ES_RETAIN=1 ES_RETAIN_MAX=4096 "$BIN" 10000 coast 20000 1 > flights/bound4096_10000_coast_20000_1.txt 2>&1

# 2. The burn ladder (the decisive experiment; knee vs N at matched cut 20,000 game-s).
ladder() { # ladder <N> <seed> <caps...>
  local N=$1 s=$2; shift 2
  local f=${N}_burn_20000_${s}
  env -u ES_LAZY_ENTRY -u ES_RETAIN -u ES_RETAIN_MAX -u ES_MINT_WHO -u ES_RETAIN_ONCE "$BIN" $N burn 20000 $s > flights/ctl_$f.txt 2>&1
  env -u ES_RETAIN_MAX -u ES_MINT_WHO -u ES_RETAIN_ONCE ES_LAZY_ENTRY=1 ES_RETAIN=1 "$BIN" $N burn 20000 $s > flights/retain_$f.txt 2>&1
  local S
  for S in "$@"; do
    env -u ES_MINT_WHO -u ES_RETAIN_ONCE ES_LAZY_ENTRY=1 ES_RETAIN=1 ES_RETAIN_MAX=$S "$BIN" $N burn 20000 $s > flights/bound${S}_$f.txt 2>&1
  done
}
ladder 10000 1 4096 16384 32768 65536
ladder 100000 1 16384 65536 131072 262144
ladder 200000 1 16384 65536 131072 262144
ladder 100000 3 16384

# 3. Kick-anchored admission (ES_RETAIN_ONCE): the admission-family refutation.
for S in 16384 65536; do
  env -u ES_MINT_WHO ES_LAZY_ENTRY=1 ES_RETAIN=1 ES_RETAIN_ONCE=1 ES_RETAIN_MAX=$S "$BIN" 100000 burn 20000 1 > flights/once${S}_100000_burn_20000_1.txt 2>&1
done
env -u ES_MINT_WHO ES_LAZY_ENTRY=1 ES_RETAIN=1 ES_RETAIN_ONCE=1 ES_RETAIN_MAX=4096 "$BIN" 100000 coast 48000 1 > flights/once4096_100000_coast_48000_1.txt 2>&1
env -u ES_MINT_WHO ES_LAZY_ENTRY=1 ES_RETAIN=1 ES_RETAIN_ONCE=1 ES_RETAIN_MAX=4096 "$BIN" 10000 coast 20000 1 > flights/once4096_10000_coast_20000_1.txt 2>&1
# ONCE needs its own coast reference at 48k (b0ed's table has the FIFO arm only):
env -u ES_RETAIN_MAX -u ES_MINT_WHO -u ES_RETAIN_ONCE ES_LAZY_ENTRY=1 ES_RETAIN=1 "$BIN" 100000 coast 48000 1 > flights/retain_100000_coast_48000_1.txt 2>&1

# 4. The reader decomposition (who mints, who hits; ES_MINT_WHO=2 samples backtraces).
ES_LAZY_ENTRY=1 ES_RETAIN=1 ES_MINT_WHO=2 "$BIN" 10000 burn 20000 1 > flights/who_retain_10000_burn_20000_1.txt 2>&1
ES_LAZY_ENTRY=1 ES_RETAIN=1 ES_MINT_WHO=2 "$BIN" 100000 burn 20000 1 > flights/who_retain_100000_burn_20000_1.txt 2>&1
ES_LAZY_ENTRY=1 ES_RETAIN=1 ES_MINT_WHO=1 "$BIN" 10000 coast 20000 1 > flights/who_retain_10000_coast_20000_1.txt 2>&1

# 5. The table (fixed: run from the run folder, write inside flights/, fail on error).
python3 "$RUNDIR/table.py" > "$RUNDIR/flights/table.txt"
echo "REGEN DONE"
