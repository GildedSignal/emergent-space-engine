#!/usr/bin/env bash
# Regenerates every dossier number: builds the harness from work/patch.diff (applied by
# the runner before this runs), flies the three arms in parallel, analyzes. Wall ~13 min
# (MAIN dominates; CTRL and SEED are cheaper and run alongside).
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
RUN=lab/results/20261020-1326-dynamics-3ea5
git apply --check "$RUN/work/patch.diff" 2>/dev/null && git apply "$RUN/work/patch.diff" || true
cargo build --release --example coretail
B="$CARGO_TARGET_DIR/release/examples/coretail"; [ -x "$B" ] || B=target/release/examples/coretail
cd "$RUN/work"
rm -rf flights; mkdir flights; cd flights
"$B" --horizon 2048 --seed 1 --thermal 0 --out SMOKE > SMOKE.log 2>&1
"$B" --horizon 147456 --seed 1 --thermal 0 --out MAIN_cold_s1 > MAIN.log 2>&1 &
P1=$!
"$B" --horizon 147456 --seed 1 --thermal 0 --pass --out CTRL_pass_s1 > CTRL.log 2>&1 &
P2=$!
"$B" --horizon 98304 --seed 2 --thermal 4096 --out SEED_th_s2 > SEED.log 2>&1 &
P3=$!
wait $P1 $P2 $P3
cd ..
python3 analyze.py MAIN_cold_s1 CTRL_pass_s1 SEED_th_s2 > analysis.txt
cat analysis.txt
grep -H contacts flights/*.head | sed 's/^.*flights\///'
