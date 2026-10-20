#!/usr/bin/env bash
# Regen for 20261020-1326-inversion-3b88 (~9 min). The two print-only ignored tests
# (b13_escape_refusal, b13_draw_scan) come from work/patch.diff; apply it if absent
# (idempotent: skipped when already applied). NOTE: B13's step-9 FAIL is the run's
# own subject, and `behave` exits 1 on a failed gate — that exit is expected and
# must not kill the regen (it is what broke the first attempt).
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root
out="lab/results/20261020-1326-inversion-3b88"

patch="$out/work/patch.diff"
if git apply --check "$patch" 2>/dev/null; then
  git apply "$patch"
fi

# 1. The gate itself at the anomaly and its brackets (dossier item 1)
for s in 8 9 10; do
  echo "=== gate step $s ===" | tee "$out/gate-$s.txt"
  PLANE_TRACE=1 cargo run --release -q -p xtask -- behave --law plane --gates B13 --plane-step "$s" 2>&1 \
    | grep -E "^plane_trace step_log2=$s |^B13 " | tee -a "$out/gate-$s.txt" || true
done

# 2. The failing row, identified (dossier item 2; shipped diagnostic)
echo "=== by_draw step 9 ===" | tee "$out/bydraw-9.txt"
B13_STEP=9 cargo test --release -p xtask b13_by_draw -- --ignored --nocapture 2>&1 \
  | grep -E "^(draw|step) " | tee -a "$out/bydraw-9.txt"

# 3. The mechanism walk, draw 27 at steps 8/9/10 (dossier item 3; this run's patch)
echo "=== escape_refusal ===" | tee "$out/escape.txt"
cargo test --release -p xtask b13_escape_refusal -- --ignored --nocapture 2>&1 \
  | grep -E "^(draw|step) " | tee -a "$out/escape.txt"

# 4. Prevalence: every draw of the stream, three octaves (dossier item 4; patch)
for s in 8 9 10; do
  echo "=== scan step $s ===" | tee "$out/scan-$s.txt"
  B13_STEP=$s cargo test --release -p xtask b13_draw_scan -- --ignored --nocapture 2>&1 \
    | grep -E "^(draw|step) " | tee -a "$out/scan-$s.txt"
done
cat "$out/scan-8.txt" "$out/scan-10.txt" > "$out/scan-8-10.txt"

echo "done; numbers are in $out/{gate-*,bydraw-9,escape,scan-*}.txt"
