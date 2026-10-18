#!/bin/sh
# Regen: every dossier number, from shipped code + work/patch.diff (applied by the runner before
# this runs). The patch adds, additively: the sky-record server in crates/universe/src/view.rs
# (read-only on the Universe), the skyserv driver module in xtask, and one dispatch arm.
# Linux/x86 shared box: orders of magnitude only. ~12 min total (build ~1 min; flights ~10 min).
set -e
cd "$(dirname "$0")/../../.."   # the repo root
R=$(pwd); W=$R/lab/results/20261018-2155-second-20261018-2040-system-cc75-e6c9/work
mkdir -p "$W"
git apply --allow-empty "$R/lab/results/20261018-2155-second-20261018-2040-system-cc75-e6c9/work/patch.diff" 2>/dev/null || true
cargo build --release -p xtask
T=$(cargo metadata --no-deps --format-version 1 | python3 -c "import json,sys; print(json.load(sys.stdin)['target_directory'])")/release/xtask
# The original run's unpatched bench digest, for the digest-neutrality cross-check.
git show origin/claude/lab-20261018-2040-system-cc75:lab/results/20261018-2040-system-cc75/work/bench0.json > "$W/orig_bench0.json"
# The decisive arms (serve = the record flying beside the oracle gather; ctl = the same flight without it).
$T universe --skyserv 1000   120 1 8e-3 1 0.5 > "$W/serve1000.log"        2>&1
$T universe --skyserv 10000  90  1 8e-3 1 0.5 > "$W/serve10000.log"       2>&1
$T universe --skyserv 100000 40  1 8e-3 1 0.5 > "$W/serve100000.log"      2>&1
$T universe --skyserv 100000 40  1 1e-3 1 0.5 > "$W/serve100000_f1e3.log" 2>&1
$T universe --skyserv 300000 20  1 8e-3 1 0.5 > "$W/serve300000.log"      2>&1
$T universe --skyserv 10000  90  7 8e-3 1 0.5 > "$W/serve10000_seed7.log" 2>&1
$T universe --skyserv 10000  90  1 8e-3 0 0.5 > "$W/ctl10000.log"         2>&1
$T universe --skyserv 100000 40  1 8e-3 0 0.5 > "$W/ctl100000.log"        2>&1
$T universe --skyserv 300000 20  1 8e-3 0 0.5 > "$W/ctl300000.log"        2>&1
$T universe --bench --seed 1 --rtf 100 --seconds 2 --unpaced > "$W/bench0.json" 2>&1

python3 "$R/lab/results/20261018-2155-second-20261018-2040-system-cc75-e6c9/analyze.py" > "$R/lab/results/20261018-2155-second-20261018-2040-system-cc75-e6c9/metrics.json" && head -c 2000 "$R/lab/results/20261018-2155-second-20261018-2040-system-cc75-e6c9/metrics.json"