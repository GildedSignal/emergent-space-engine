#!/bin/bash
# Regenenerates every number in dossier.md from the shipped tree + work/patch.diff (applied by the
# runner before this runs). ~4-5 min: one warm build, two timed runs, one digest identity check.
# NOTE: `--examples` (all) fails on this commit: the `nladder` example links the macOS-only
# proc_pid_rusage (pre-existing on main). Build the two portable examples by name.
set -euo pipefail
R="$(cd "$(dirname "$0")" && pwd)"     # this run's folder (absolute)
cd "$R/../../.."                       # repo root: lab/results/<id> -> up 3

echo "== machine =="
cat /proc/loadavg; grep "model name" /proc/cpuinfo | head -1

echo "== build (patch is already applied by the runner) =="
cargo build --release -p emergent-universe --example birth_rail --example ladder_digest

B="$CARGO_TARGET_DIR/release/examples/birth_rail"
L="$CARGO_TARGET_DIR/release/examples/ladder_digest"

echo "== the decisive run: seed 1, N ladder (slope + ES_BIRTH_SPLIT stages) =="
ES_BIRTH_SPLIT=1 REPS=3 "$B" 0 10000 100000 300000 2>&1 | tee "$R/run_main.log"

echo "== held-out seed 3 =="
SEED=3 REPS=2 ES_BIRTH_SPLIT=1 "$B" 10000 100000 2>&1 | tee "$R/run_seed3.log"

echo "== the table =="
python3 "$R/analysis.py" "$R/run_main.log"
python3 "$R/analysis.py" "$R/run_seed3.log"

echo "== digest identity: patched tree, ES off (13 cases x 4 schedules) =="
"$L" | tee "$R/ld_patched.txt"

echo "== digest identity vs pristine at the same commit (git stash overlay) =="
git stash push -q -m birthsplit-pristine -- crates/universe/src/lib.rs crates/universe/src/universe.rs crates/universe/src/scenario.rs
trap 'git stash pop -q || true' EXIT
cargo build --release -p emergent-universe --example ladder_digest
"$L" | tee "$R/ld_pristine.txt"
git stash pop -q
trap - EXIT
cargo build --release -p emergent-universe --example ladder_digest
# Identity = digests and kick/encounter/contact counters match; the trailing wall-time
# column ([X.X s]) is timing, not physics, so it is stripped before the comparison.
norm() { sed 's/ *\[[0-9.]* s\]$//' "$1"; }
if diff <(norm "$R/ld_patched.txt") <(norm "$R/ld_pristine.txt") > "$R/ld_diff.txt"; then
  echo "DIGEST IDENTITY: patched == pristine (digests and counters; wall-time column excluded)"
else
  echo "DIGEST MISMATCH (digests or counters differ):"; cat "$R/ld_diff.txt"
fi
echo "done."
