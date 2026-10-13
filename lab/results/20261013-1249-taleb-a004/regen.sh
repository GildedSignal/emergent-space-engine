#!/usr/bin/env bash
# Regenerates every number in dossier.md: the 20-arm matrix (~15 s), the analysis, and the
# decision-tick regression tests. Run after work/patch.diff is applied. Cold build ~3 min,
# matrix 15 s, tests ~10 s; every arm is deterministic (Budget::events arms), so digests
# reproduce bit for bit on any machine.
set -e
cd "$(dirname "$0")/../../.."  # repo root
W=lab/results/20261013-1249-taleb-a004/work
cargo build --release -p emergent-universe --example ruin_probe
cargo build --release -p xtask  # proves the session.rs / kick_bench wiring compiles
for arm in \
  "raw 11 60 0 84000000 100 48 std" "raw 11 60 1 84000000 100 48 std" \
  "raw 11 30 0 84000000 100 48 std" "raw 11 144 0 84000000 100 48 std" \
  "raw 11 60 0 252000000 100 48 std" "raw 11 60 1 252000000 100 48 std" \
  "raw 11 60 0 756000000 100 48 std" "raw 11 60 1 756000000 100 48 std" \
  "fix 11 60 0 84000000 100 48 std" "fix 11 60 1 84000000 100 48 std" \
  "fix 11 30 0 84000000 100 48 std" "fix 11 144 0 84000000 100 48 std" \
  "fix 11 60 0 84000000 1 48 std" "fix 11 60 1 84000000 1 48 std" \
  "fix 11 30 0 84000000 100 48 straddle" "fix 11 144 0 84000000 100 48 straddle" \
  "raw 11 60 0 84000000 100 400 std" "raw 11 60 1 84000000 100 400 std" \
  "fix 11 60 0 84000000 100 400 std" "fix 11 60 1 84000000 100 400 std"; do
  timeout 60 cargo run --release -p emergent-universe --example ruin_probe -- $arm
done > $W/matrix.txt
python3 $W/analyze.py $W/matrix.txt | tee $W/summary.txt
grep -c HELD $W/summary.txt  # 6/6 expected
cargo test --release -p emergent-universe --test decision_tick 2>&1 | tail -3
