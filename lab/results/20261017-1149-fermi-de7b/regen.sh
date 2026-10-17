#!/bin/sh
# Regenerates every number in the dossier. The runner applies work/patch.diff (adds
# crates/universe/examples/belt_combs.rs) before this runs. Three arms of the decisive
# experiment (N = 10^4, three octaves of the shipped step lever), then the 10^9 ledger
# arithmetic. Total: well under 15 minutes (build ~2 min, ~30 s per arm).
set -e
# cd to the repo root: walk up from this script until Cargo.toml appears (the checkout
# root is 3 levels up here, but don't hardcode depth).
root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
while [ "$root" != "/" ] && [ ! -f "$root/Cargo.toml" ]; do root=$(dirname -- "$root"); done
cd "$root"
cargo build --release -p emergent-universe --example belt_combs
run() { cargo run --release -p emergent-universe --example belt_combs -- "$@"; }
run 10000 2400 20000 60000 7   # shipped lever: scan between the combs, end past 2 intervals
run 10000 2400 40000 58000 8   # one octave finer: scan between kick 5 and boundary 3
run 10000 2400 40000 58000 6   # one octave coarser: scan between kick 1 and boundary 1
python3 lab/results/20261017-1149-fermi-de7b/ledger.py
