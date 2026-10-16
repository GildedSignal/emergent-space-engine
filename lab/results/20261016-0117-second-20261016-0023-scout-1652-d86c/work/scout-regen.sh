#!/bin/sh
# Regen (20261016-0023-scout-1652): every dossier number from shipped code + this run's patch
# (work/patch.diff is applied by the runner before this runs). One build, three flights, ~35 s.
set -e
cd "$(dirname "$0")/../../.."   # the repo root
cargo build --release -p emergent-universe --example history_window
BIN="${CARGO_TARGET_DIR:-$HOME/lab-target-2}/release/examples/history_window"
R=lab/results/20261016-0023-scout-1652
# the census: four cuts past the first wave (the dossier table)
"$BIN" 10000 1500 15000 20000 32000 48000 > "$R/census_n10k.log"
# control (a): a cut inside the wave's window must read IN_WINDOW high (the transient)
"$BIN" 10000 1500 13800 > "$R/census_wave_control.log"
# control (b): the pinned fraction is high at a second population size
"$BIN" 3000 1500 32000 > "$R/census_n3k.log"
echo "regen done"
