#!/bin/sh
# Regen (959a): rebuild and fly every number in dossier.md from the shipped tree + work/patch.diff.
# work/patch.diff = e6c9's sky_server probe (verbatim from its published branch, commit 5908e300)
# + this run's running-sums serve tier (ES_SKY_SUMS gate; unset = e6c9 verbatim).
# Wall ≈ 11 min on the lab box. Every flight ≤ 60 s where possible (the oracle gather, the audit
# instrument, dominates the top rungs; 3e5 is one process ~2.8 min, as in e6c9's own grid).
set -e
cd "$(dirname "$0")"
RUN="$(pwd)"
ROOT="$(git rev-parse --show-toplevel)"          # patch paths are repo-root-relative
cd "$ROOT"
git apply -R "$RUN/work/patch.diff" 2>/dev/null || true   # idempotent re-apply below
git apply "$RUN/work/patch.diff"
cargo build --release -q -p xtask
mkdir -p "$RUN/work/logs"
B="cargo run --release -q -p xtask -- universe --skyserv"
cd "$RUN/work/logs"
ES_SKY_SUMS=1 $B 1000 120 1 8e-3 1 0.5 > sum1000.log 2>&1
$B 10000 90 1 8e-3 1 0.5 > ctl10000.log 2>&1
ES_SKY_SUMS=1 $B 10000 90 1 8e-3 1 0.5 > sum10000.log 2>&1
$B 100000 40 1 8e-3 1 0.5 > ctl100000.log 2>&1
ES_SKY_SUMS=1 $B 100000 40 1 8e-3 1 0.5 > sum100000.log 2>&1
ES_SKY_SUMS=1 $B 300000 20 1 8e-3 1 0.5 > sum300000.log 2>&1
ES_SKY_SUMS=1 $B 10000 90 1 1e-3 1 0.5 > sum10000_f1e3.log 2>&1
ES_SKY_SUMS=1 $B 10000 300 1 8e-3 1 0.5 > sum10000_long.log 2>&1
$B 10000 90 1 8e-3 0 0.5 > ctl_noserve.log 2>&1
ES_SKY_SUMS=1 $B 100000 40 7 8e-3 1 0.5 > sum100000_seed7.log 2>&1
python3 "$RUN/work/analyze.py"                    # the table the dossier quotes
echo "REGEN DONE"
