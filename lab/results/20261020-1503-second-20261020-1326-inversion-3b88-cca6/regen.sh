#!/usr/bin/env bash
# Regen for 20261020-1503-second-20261020-1326-inversion-3b88-cca6 (second author on 3b88;
# ~11 min from a clean tree). Two standalone patches, applied in order, each skipped when
# already present:
#   work/tests.diff   — 3b88's two print-only ignored tests (byte-identical to its work/fix.diff)
#   work/wall-fix.diff— the one-branch fix class: a periapsis past every representable tick
#                       reads as Ok(None) in next_periapsis (crates/universe/src/step.rs)
# Baseline (shipped law) first, then the fixed flight. A gate FAIL exit is a datum, not an
# error: `behave` exits 1 on FAIL, and pipefail would propagate it through tee, so every
# gate pipeline carries an explicit `|| true`.
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root
out="lab/results/20261020-1503-second-20261020-1326-inversion-3b88-cca6"

apply() { git apply --check "$1" 2>/dev/null && git apply "$1" || echo "already applied: $1"; }

# ---------- baseline: shipped law, tests only ----------
apply "$out/work/tests.diff"
cargo build --release -p xtask >/dev/null 2>&1

echo "=== baseline gate step 9 ===" | tee "$out/base-gate-9.txt"
PLANE_TRACE=1 cargo run --release -q -p xtask -- behave --law plane --gates B13 --plane-step 9 2>&1 \
  | grep -E "^plane_trace step_log2=9 lost|^B13 " | tee -a "$out/base-gate-9.txt" || true

echo "=== baseline escape walk draw 27 step 9 ===" | tee "$out/base-escape-9.txt"
B13_STEPS=9 cargo test --release -p xtask b13_escape_refusal -- --ignored --nocapture 2>&1 \
  | grep -E "^(draw|step) " | tee -a "$out/base-escape-9.txt"

echo "=== baseline scan step 9 ===" | tee "$out/base-scan-9.txt"
B13_STEP=9 cargo test --release -p xtask b13_draw_scan -- --ignored --nocapture 2>&1 \
  | grep -E "^(draw|step) " | tee -a "$out/base-scan-9.txt"

# ---------- fixed flight: the wall fix applied ----------
apply "$out/work/wall-fix.diff"
cargo build --release -p xtask >/dev/null 2>&1

for s in 8 9 10; do
  echo "=== fixed gate step $s ===" | tee "$out/fix-gate-$s.txt"
  PLANE_TRACE=1 cargo run --release -q -p xtask -- behave --law plane --gates B13 --plane-step "$s" 2>&1 \
    | grep -E "^plane_trace step_log2=$s lost|^B13 " | tee -a "$out/fix-gate-$s.txt" || true
done

echo "=== fixed escape walk draw 27 steps 8,9,10 ===" | tee "$out/fix-escape.txt"
B13_STEPS=8,9,10 cargo test --release -p xtask b13_escape_refusal -- --ignored --nocapture 2>&1 \
  | grep -E "^(draw|step) " | tee -a "$out/fix-escape.txt"

for s in 9 8 10 7; do
  echo "=== fixed scan step $s ===" | tee "$out/fix-scan-$s.txt"
  B13_STEP=$s cargo test --release -p xtask b13_draw_scan -- --ignored --nocapture 2>&1 \
    | grep -E "^(draw|step) " | tee -a "$out/fix-scan-$s.txt"
done

echo "=== fixed by_draw step 9 ===" | tee "$out/fix-bydraw-9.txt"
B13_STEP=9 cargo test --release -p xtask b13_by_draw -- --ignored --nocapture 2>&1 \
  | grep -E "^(draw|step) " | tee -a "$out/fix-bydraw-9.txt"

echo "done; numbers are in $out/{base-*,fix-*}.txt"
