#!/usr/bin/env bash
# Regen for 20261016-1740-taleb-a8cd: every dossier number, from shipped code + work/patch.diff.
# Core ≈ 6 min. REGEN_FULL=1 adds the whole-suite failure count (~9 min more).
set -uo pipefail
cd "$(dirname "$0")/../../.."
R=lab/results/20261016-1740-taleb-a8cd

echo "=== 0. patch (three #[ignore] probes + libm dev-dep) ==="
git apply --check "$R/work/patch.diff" 2>/dev/null && git apply "$R/work/patch.diff" && echo applied || echo "already applied (this run's own tree)"

echo "=== 1. the deterministic seven: names + messages (corpus drift, B12-false, across_a_kick) ==="
cargo test -p xtask -- behave::handoff::tests echo_passes_the_four_events across_a_kick_the_register --nocapture 2>&1 \
  | grep -E "panicked at|^\[[0-9].*\]$|left:|right:|starts at zero|^ship [0-9]|handoffs: 16 frozen|test .* \.\.\. (ok|FAILED)" | head -40

echo "=== 2. the flaky three (load class): pass when run alone ==="
cargo test -p xtask -- the_other_gates_can_fail_too each_planted_law_fails_exactly echo_is_linear_and 2>&1 | grep -E "test .* \.\.\. (ok|FAILED)" | head

echo "=== 3. the corpus census: pristine / ±1 ulp / musl (the machine channel) ==="
cargo test -p xtask lab_corpus_ulp_libm_census -- --ignored --nocapture 2>&1 | grep -E "kept\[|judged \("

echo "=== 4. the selection probe: which ships the failing test judges here ==="
cargo test -p xtask lab_across_a_kick_selection -- --ignored --nocapture 2>&1 | grep -E "kept\[|filtered#"

echo "=== 5. the ulp-stability control: the failing ship's walk under ±1 ulp ==="
cargo test -p xtask lab_across_a_kick_ulp_stability -- --ignored --nocapture 2>&1 | grep -E "pristine|all.1ulp"

echo "=== 6. the freeze-commit control: the same test at c84f5787 (6 Oct) on this box ==="
[ -d "$R/work/tree610" ] || git worktree add "$R/work/tree610" c84f5787 >/dev/null 2>&1
cd "$R/work/tree610" && CARGO_TARGET_DIR=/home/glmlab/lab-target-3/tree610 cargo test -p xtask across_a_kick_the_register -- --nocapture 2>&1 \
  | grep -E "^ship [0-9]|across_kick_over_work" | head -8
cd - >/dev/null

echo "=== 7. the CR check: glibc vs correctly-rounded on the seeds where musl differs ==="
pip install mpmath -q 2>/dev/null; python3 "$R/work/crcheck.py"

if [ "${REGEN_FULL:-0}" = 1 ]; then
  echo "=== 8. FULL suite failure count (optional, ~9 min) ==="
  cargo test -p xtask -j 6 2>&1 | grep -E "test result:" | tail -2
fi
echo "REGEN DONE"
