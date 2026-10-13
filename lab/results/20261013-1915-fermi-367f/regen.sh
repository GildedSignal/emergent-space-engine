#!/usr/bin/env bash
# Regen: rebuild with the probe patch, rerun the ladder, re-derive every number in the dossier.
# ≤ 15 min on a Linux/x86 box (uses $CARGO_TARGET_DIR if set). Keep every process under 2 GB.
set -euo pipefail
cd "$(dirname "$0")"                # lab/results/<id>
cd "$(git rev-parse --show-toplevel)"  # repo root (was ../.., which stopped in lab/)
RUN=lab/results/20261013-1915-fermi-367f

git apply --check "$RUN/work/patch.diff" 2>/dev/null || { echo "patch check failed; restoring touched files" >&2; git checkout -- xtask/src/universe/mod.rs 2>/dev/null || true; }
git apply "$RUN/work/patch.diff"

cargo build --release -p xtask --features emergent-universe/prof
X="${CARGO_TARGET_DIR:-target}/release/xtask"

mkdir -p "$RUN/data"
cd "$RUN"
for m in 48 400 1500; do "$X" universe --bench --seconds 8 --rtf 100 --members "$m" > "data/r100-m$m.json" 2>&1; done
"$X" universe --bench --seconds 4 --rtf 100 --members 4000 > data/r100-m4000.json 2>&1
for m in 48 400 1500 4000; do "$X" universe --bench --seconds 8 --rtf 1 --members "$m" > "data/r1-m$m.json" 2>&1; done
for m in 400 1500; do "$X" universe --bench --seconds 8 --rtf 100 --members "$m" --seed 3 > "data/r100-m$m-s3.json" 2>&1; done

python3 analyze.py | tee ladder-table.txt
echo "regen done: compare ladder-table.txt against dossier.md's table (orders of magnitude; shared box)"
