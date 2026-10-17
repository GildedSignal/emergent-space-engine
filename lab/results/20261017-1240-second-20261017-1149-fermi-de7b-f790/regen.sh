#!/bin/sh
# Regenerates every number in the dossier. The runner applies work/patch.diff before this
# runs: de7b's belt_combs instrument (plus this run's <seed> argument, the h<60k/h>=60k
# mixture counter and the 140-s flight guard) and 98cb's BELT_SPLIT patch on the crates
# (both toggles env-gated, off unless set; IMPACT_GUESS=0 keeps next_impact on the shipped
# bisection everywhere). Six flights + ledger: ~5 min on an unloaded box, ~10 min loaded.
set -e
root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
while [ "$root" != "/" ] && [ ! -f "$root/Cargo.toml" ]; do root=$(dirname "$root"); done
cd "$root"
export IMPACT_GUESS=0   # 98cb's crash-search guess off: the shipped bisection everywhere
cargo build --release -p emergent-universe --example belt_combs
run() { cargo run --release -p emergent-universe --example belt_combs -- "$@"; }
run 10000 2400 20000 60000 7 1    # shipped lever, seed 1: the record check (de7b's arm 7)
run 10000 2400 40000 58000 6 1    # one octave coarser: de7b's arm 6 scan point
run 10000 2400 40000 58000 8 1    # one octave finer: de7b's arm 8 scan point
run 10000 2400 20000 60000 7 2    # seed 2 (checker's named miss: one seed only)
run 10000 2400 20000 60000 7 3    # seed 3
BELT_SPLIT=1 cargo run --release -p emergent-universe --example belt_combs -- 10000 24000 160000 460000 7 1   # the direct split flight (checker's named experiment)
python3 lab/results/20261017-1240-second-20261017-1149-fermi-de7b-f790/ledger.py
