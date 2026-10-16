#!/usr/bin/env bash
# Regen for 20261016-1835-second-20261016-1740-taleb-a8cd-32a1 (second author).
# Fixes the parent's delivery hole: patch.diff no longer adds any workspace member, so every
# `cargo test -p xtask` below actually runs; `set -e` + grep-or-die per step means a step that
# produces nothing kills the script instead of exiting 0 vacuously (the parent's silver cause).
# Steps 1-5 reproduce the parent's numbers bit for bit; step 5b is the checker's named missing
# experiment (the CR-only seed path). Core ≈ 12 min. REGEN_FULL=1 adds the suite (~10 min more).
set -euo pipefail
R="$(cd "$(dirname "$0")" && pwd)"
cd "$R/../../.."
exec > >(tee "$R/regen.log") 2>&1
echo "=== 0. patch (five #[ignore] probes + libm dev-dep; NO workspace member) ==="
if git apply --check "$R/work/patch.diff" 2>/dev/null; then git apply "$R/work/patch.diff" && echo applied; else echo "already applied (this run's own tree)"; fi

echo "=== 1. the deterministic seven: names + messages (corpus drift, B12-false, across_a_kick) ==="
(cargo test -p xtask -- behave::handoff::tests echo_passes_the_four_events across_a_kick_the_register --nocapture 2>&1 || true) \
  | grep -E "panicked at|^\[[0-9].*\]$|left:|right:|starts at zero|^ship [0-9]|handoffs: 16 frozen|test .* \.\.\. (ok|FAILED)" | head -40

echo "=== 2. the flaky three (load class): pass when run alone ==="
(cargo test -p xtask -- the_other_gates_can_fail_too each_planted_law_fails_exactly echo_is_linear_and 2>&1 || true) | grep -E "test .* \.\.\. (ok|FAILED)" | head

echo "=== 3. the corpus census: pristine / ±1 ulp / musl (the machine channel) ==="
(cargo test -p xtask lab_corpus_ulp_libm_census -- --ignored --nocapture 2>&1 || true) | grep -E "kept\[|judged \("

echo "=== 4. the selection probe: which ships the failing test judges here ==="
(cargo test -p xtask lab_across_a_kick_selection -- --ignored --nocapture 2>&1 || true) | grep -E "kept\[|filtered#"

echo "=== 5. the ulp-stability control: the failing ship's walk under ±1 ulp ==="
(cargo test -p xtask lab_across_a_kick_ulp_stability -- --ignored --nocapture 2>&1 || true) | grep -E "pristine|all.1ulp"

echo "=== 5b. the CR-only seed path (the checker's named missing experiment) ==="
python3 -c "import mpmath" 2>/dev/null || pip install mpmath -q
python3 "$R/work/crseeds.py" > "$R/work/cr_seeds.txt"
echo "cr_seeds.txt sha256: $(sha256sum "$R/work/cr_seeds.txt" | cut -d' ' -f1)"
export CR_TABLE="$R/work/cr_seeds.txt"
(cargo test -p xtask lab_corpus_cr_seeds -- --ignored --nocapture 2>&1 || true) | grep -E "kept\[|CR corpus"
(cargo test -p xtask lab_across_a_kick_cr_seeds -- --ignored --nocapture 2>&1 || true) | grep -E "CR kept"

echo "=== 6. the freeze-commit control: the same test at c84f5787 (6 Oct) on this box ==="
T610="${T610:-/home/glmlab/lab-tree610-32a1}"
if [ ! -f "$T610/Cargo.toml" ]; then git worktree add --detach "$T610" c84f5787 >/dev/null 2>&1; fi
(cd "$T610" && CARGO_TARGET_DIR="${T610_TARGET:-/home/glmlab/lab-target-3/tree610}" cargo test -p xtask across_a_kick_the_register -- --nocapture 2>&1 || true) \
  | grep -E "^ship [0-9]|across_kick_over_work" | head -8

echo "=== 7. the CR check: glibc vs correctly-rounded on the seeds where musl differs ==="
python3 "$R/work/crcheck.py"

if [ "${REGEN_FULL:-0}" = 1 ]; then
  echo "=== 8. FULL suite failure count (optional) ==="
  (cargo test -p xtask -j 6 2>&1 || true) | grep -E "test result:" | tail -2
fi
echo "REGEN DONE"
