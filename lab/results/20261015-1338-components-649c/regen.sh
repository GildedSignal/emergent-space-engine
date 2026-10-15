#!/bin/sh
# Regenerates every number in dossier.md from the shipped tree plus this run's instrument.
# ~7-8 min on a quiet 8-vCPU box (the 10^5 arms own ~4.5 min of it). Each flight is one
# process under ~600 MB; needs only cargo.
set -e
cd "$(dirname "$0")/../../.."   # repo root

# the instrument (this run's only tree edit; identical to work/view_floor.rs and work/patch.diff)
cp -f lab/results/20261015-1338-components-649c/work/view_floor.rs crates/universe/examples/view_floor.rs
cargo build --release -p emergent-universe --example view_floor >/dev/null
BIN=$(ls -t ./target/release/examples/view_floor /home/glmlab/lab-target-*/release/examples/view_floor 2>/dev/null | head -1)
echo "instrument: $BIN"

OUT=lab/results/20261015-1338-components-649c/out
mkdir -p "$OUT"
: > "$OUT"/grid.log

# the grid (dossier table + the staircase evidence run); N, mode, frames, rtf[, freeze frame]
run() { echo "=== $*" | tee -a "$OUT"/grid.log; "$BIN" "$@" 2>/dev/null | tee -a "$OUT"/grid.log | tail -16; }
run 1000 coast 300 100          # anchor arm: price + floor at 10^3
run 1000 burn8 300 100          # the burn at L8
run 10000 coast 260 100         # the crawl's first rung: the gather owns 99.8% of the flown frame
run 10000 burn8 260 100
run 10000 burn15 260 100        # the extreme burn: far rows still bit-frozen, same quantum step
run 1000 coast 1000 100 100     # the staircase: exact >=213 frames, first step 355-542 game-s
run 100000 coast 80 100         # the crawl at 10^5 (the rtf-0.7 class)
run 100000 burn8 80 100

echo "done: $OUT/grid.log"
