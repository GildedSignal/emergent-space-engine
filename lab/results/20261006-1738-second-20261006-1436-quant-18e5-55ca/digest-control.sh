#!/bin/bash
# Two digest controls:
#  A) my instrumentation patch is measurement-only: same commit, universe.rs stashed vs not, same digest.
#  B) the original e record regenerates at the author's base commit 110c3e0 (clean tree).
set -eu
cd "$(dirname "$0")/../../.." || exit 1
R=lab/results/20261006-1738-second-20261006-1436-quant-18e5-55ca/data
DG () { python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(d['digest'][:16],'@',d['cut_tick'])" "$1"; }

echo "=== A: patch-no-op (HEAD=$(git rev-parse --short HEAD))"
git stash push -m lab-second-aux -- crates/universe/src/universe.rs >/dev/null
cargo build --release -p xtask 2>&1 | tail -1
/home/glmlab/lab-target-3/release/xtask universe --bench --seed 1 --rtf 100 --members 480 --level 15 --seconds 30 > "$R/A-clean.json" 2>/dev/null
echo "clean-universe.rs digest: $(DG "$R/A-clean.json")"
git stash pop >/dev/null
cargo build --release -p xtask 2>&1 | tail -1

echo "=== B: author base 110c3e0, clean"
git stash push -m lab-second-all >/dev/null
git checkout -q 110c3e0
cargo build --release -p xtask 2>&1 | tail -1
/home/glmlab/lab-target-3/release/xtask universe --bench --seed 1 --rtf 100 --members 480 --level 15 --seconds 30 > "$R/B-base.json" 2>/dev/null
echo "base-commit digest:      $(DG "$R/B-base.json")"
git checkout -q - 
git stash pop >/dev/null
cargo build --release -p xtask 2>&1 | tail -1
echo "=== restored $(git rev-parse --short HEAD), instrumented again:"
/home/glmlab/lab-target-3/release/xtask universe --bench --seed 1 --rtf 100 --members 480 --level 15 --seconds 5 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print('sanity digest:', d['digest'][:16], '(expect 761f6900 for the 5s cut)')"
