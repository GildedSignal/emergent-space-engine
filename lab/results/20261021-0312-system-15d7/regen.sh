#!/bin/sh
# Run 20261021-0312-system-15d7: regenerate every dossier number from a clean tree.
# The runner applies work/patch.diff (the print-only counters + this example) before running.
set -e
cd "$(dirname "$0")/../../.."   # repo root

echo "== build (instrumented example)"
cargo build --release -p emergent-universe --example boundary_bill 2>&1 | tail -1

echo "== 1. belt, completed flight (3e4 bodies; horizon arg is wall-s at rtf 100 = 500,000 game-s
#     ~= 18 eras; ~111 s wall on the lab box)"
timeout 260 cargo run --release -p emergent-universe --example boundary_bill -- 30000 5000 \
  2>belt-err.txt | tee "$(dirname "$0")/belt-era.txt"
sed 's/ t .*//' belt-err.txt | sort | uniq -c
rm -f belt-err.txt

echo "== 2. determinism cross-check (killed at the runner's 420 s cap, as in the author's run)"
timeout 420 cargo run --release -p emergent-universe --example boundary_bill -- 30000 28000 2>belt-long-err.txt >/dev/null || echo "(killed at the 420 s cap, as in the author's run)"
sed 's/ t .*//' belt-long-err.txt | sort | uniq -c
rm -f belt-long-err.txt

echo "== 3. control: plunges (boundary fires must be absent; tests must pass)"
cargo test --release -p emergent-universe --test plunge -- --nocapture 2>&1 | grep -E "BOUNDARY FIRE|test result" | sed 's/ t .*//' | sort | uniq -c | tee "$(dirname "$0")/plunge-control.txt"

echo "done"
