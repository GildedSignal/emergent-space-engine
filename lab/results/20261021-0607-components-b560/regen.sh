#!/bin/sh
# Regen: every number in dossier.md, from shipped code + this run's patch/script.
# Wall: two builds incremental (~10 s) + two census runs (~8-18 s each) < 60 s total budget each.
set -e
cd "$(dirname "$0")/../../.."   # repo root (this script lives in lab/results/<run>/)

# 1. The patch (the example). If work/patch.diff is absent or fails, place the snapshot copy.
if [ -f lab/results/20261021-0607-components-b560/work/patch.diff ]; then
  git apply lab/results/20261021-0607-components-b560/work/patch.diff || \
    cp lab/results/20261021-0607-components-b560/family_census.rs crates/universe/examples/family_census.rs
else
  cp lab/results/20261021-0607-components-b560/family_census.rs crates/universe/examples/family_census.rs
fi

# 2. Build and run the census at both radii (each run: F=16, 6 arms, fires cap 300, wall cap 40-60 s).
cargo build --release --example family_census
B=$(cargo metadata --no-deps --format-version 1 | python3 -c "import json,sys; print(json.load(sys.stdin)['target_directory'])")/release/examples/family_census
D=lab/results/20261021-0607-components-b560
"$B" 101300000 300 40 > "$D/census-r1au.txt" 2>&1
"$B" 202600000 300 60 > "$D/census-r2au.txt" 2>&1

# 3. The dossier's headline numbers.
grep -E "^#|aligned pair" "$D/census-r1au.txt" "$D/census-r2au.txt"
grep -E "^ +(0|100|1000|10000|100000|1000000) \|" "$D/census-r1au.txt"
grep "anchor_spread" "$D/census-r1au.txt"
