#!/bin/bash
# Round 2: A2 = clean tree at 70f27a9 (all tracked edits stashed) vs the instrumented a73ef0f4 runs.
# B2 = second run at 110c3e0 (same binary rebuilt from cache) vs B1's a0746ad1: per-build determinism.
set -eu
cd "$(dirname "$0")/../../.." || exit 1
R=lab/results/20261006-1738-second-20261006-1436-quant-18e5-55ca/data
DG () { python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(d['digest'][:16],'@',d['cut_tick'])" "$1"; }
RUN () { /home/glmlab/lab-target-3/release/xtask universe --bench --seed 1 --rtf 100 --members 480 --level 15 --seconds 30 > "$1" 2>/dev/null; }

git stash push -m lab-second-r2 >/dev/null
echo "=== A2: clean $(git rev-parse --short HEAD)"
cargo build --release -p xtask 2>&1 | tail -1
RUN "$R/A2-clean-70f27a9.json"; echo "A2 digest: $(DG "$R/A2-clean-70f27a9.json") (instrumented runs gave a73ef0f45bd673fc)"

echo "=== B2: 110c3e0 again (same tree, cache build)"
git checkout -q 110c3e0
cargo build --release -p xtask 2>&1 | tail -1
RUN "$R/B2-base.json"; echo "B2 digest: $(DG "$R/B2-base.json") (B1 gave a0746ad1566a0b76)"

git checkout -q -
git stash pop >/dev/null
cargo build --release -p xtask 2>&1 | tail -1
echo "restored: $(git rev-parse --short HEAD)"
