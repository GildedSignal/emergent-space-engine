#!/bin/sh
# Run 20261021-0429-second-20261021-0312-system-15d7-e415: regenerate every dossier number from
# a clean tree. The runner applies work/patch.diff (counters + the gated deletion + the example
# + the B13 arm) before running this. Total ~11 min on the lab box.
set -e
cd "$(dirname "$0")/../../.."   # repo root
R="lab/results/20261021-0429-second-20261021-0312-system-15d7-e415"
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT

echo "== build"
cargo build --release -p emergent-universe --example boundary_bill 2>&1 | tail -1
cargo test --release -p xtask --bin xtask b13_cut --no-run 2>&1 | tail -1

echo "== 1. baseline belt flight (gate off): must reproduce 15d7's frozen record bit for bit"
timeout 400 cargo run --release -p emergent-universe --example boundary_bill -- 30000 5000 \
  2>"$R/belt-base-err.txt" | tee "$R/belt-base.txt"

echo "== 2. the deletion, same flight (ES_BOUNDARY_CUT=1)"
ES_BOUNDARY_CUT=1 timeout 400 cargo run --release -p emergent-universe --example boundary_bill -- 30000 5000 \
  2>"$R/belt-cut-err.txt" | tee "$R/belt-cut.txt"
grep "BOUNDARY FIRE" "$R/belt-base-err.txt" | sort > "$T/a"
grep "BOUNDARY FIRE" "$R/belt-cut-err.txt" | sort > "$T/b"
diff "$T/a" "$T/b" && echo "fire traces IDENTICAL ($(wc -l < "$T/a") lines)"

echo "== 3. held-out seed 7 (the first checker's own case), both arms, 200k gs"
timeout 300 cargo run --release -p emergent-universe --example boundary_bill -- 30000 2000 7 \
  2>"$R/seed7-base-err.txt" > "$R/seed7-base.txt"
ES_BOUNDARY_CUT=1 timeout 300 cargo run --release -p emergent-universe --example boundary_bill -- 30000 2000 7 \
  2>"$R/seed7-cut-err.txt" > "$R/seed7-cut.txt"
cat "$R/seed7-base.txt" "$R/seed7-cut.txt"
grep "BOUNDARY FIRE" "$R/seed7-base-err.txt" | sort > "$T/a"
grep "BOUNDARY FIRE" "$R/seed7-cut-err.txt" | sort > "$T/b"
diff "$T/a" "$T/b" && echo "seed-7 fire traces IDENTICAL ($(wc -l < "$T/a") lines)"

echo "== 4. adversarial arm: B13's assist draws (the 3b88 wall class), gate off vs on"
timeout 600 cargo test --release -p xtask --bin xtask b13_cut -- --ignored --nocapture 2>&1 \
  | grep -E "^draw |^step |test result" | tee "$R/b13-cut.txt"

echo "== 5. controls: plunges and the lib, gate off then on"
timeout 300 cargo test --release -p emergent-universe --test plunge -- --nocapture 2>&1 | grep -E "BOUNDARY FIRE|test result" | tee "$R/plunge-off.txt"
ES_BOUNDARY_CUT=1 timeout 300 cargo test --release -p emergent-universe --test plunge -- --nocapture 2>&1 | grep -E "BOUNDARY FIRE|test result" | tee "$R/plunge-on.txt"
timeout 600 cargo test --release -p emergent-universe --lib 2>&1 | grep "test result" | tee "$R/tests-off.txt"
ES_BOUNDARY_CUT=1 timeout 600 cargo test --release -p emergent-universe --lib 2>&1 | grep "test result" | tee -a "$R/tests-off.txt"
echo "(the motion suite with the gate on: 7 pass, 1 fails at motion.rs:411 — its sampler reads"
echo " 'right after a kick' THROUGH the boundary item, so it finds 0 samples; the physics"
echo " assertions never ran. The adoption patch re-points that sampler at the kick item.)"

echo "done"
