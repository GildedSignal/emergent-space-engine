#!/bin/sh
# Regen (lab run 20261014-1221-system-b8fc). The runner applies work/patch.diff first.
# Reproduces every number in dossier.md: the census on three arms plus the schedule-identity
# check. Rust release build ~15-60 s per arm after the first build; total well under 15 min.
set -e
cd "$(dirname "$0")/../../.."   # the repo root (the run folder is lab/results/<id>)
run() { cargo run --release -p emergent-universe --features prof --example knot_census -- "$@"; }

echo '== battle-paced arm: seed 3, 1500 members, rtf 100, 8 game-s, unlimited =='
run 3 1500 100 8

echo '== flying arm: seed 3, 400 members, rtf 100, 8 game-s, unlimited =='
run 3 400 100 8

echo '== schedule identity: the same arm on a biting 3 ms wall budget (digest must equal the unlimited arm) =='
run 3 400 100 8 3

echo '== rtf 1 arm (the quiet battle pace) =='
run 3 1500 1 8
