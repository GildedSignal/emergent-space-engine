#!/usr/bin/env bash
# Regenerates every number in dossier.md (logs land beside this script, in work/).
# The runner applies work/patch.diff (the skycensus probe) before this runs; if not:
set -e
cd "$(git rev-parse --show-toplevel)"
git apply --check lab/results/20261018-2155-spacex-9292/work/patch.diff 2>/dev/null && git apply lab/results/20261018-2155-spacex-9292/work/patch.diff
cargo build --release -p emergent-universe --example skycensus
B="$(cargo metadata --format-version 1 --no-deps | python3 -c 'import json,sys;print(json.load(sys.stdin)["target_directory"])')/release/examples/skycensus"
cd lab/results/20261018-2155-spacex-9292/work
"$B" 1000 coast 360 100 1 8  > c1e3.txt
"$B" 1000 burn 360 100 1 8   > b1e3.txt
"$B" 1000 burn 1500 100 1 8  > b1e3long.txt
"$B" 1000 burn 360 100 1 15  > b1e3l15.txt
"$B" 10000 coast 360 100 1 8 > c1e4.txt
"$B" 10000 burn 360 100 1 8  > b1e4.txt
"$B" 100000 burn 180 100 10 8 > b1e5.txt
echo "regen done: grep 'skycensus:' *.txt for the dossier lines"
