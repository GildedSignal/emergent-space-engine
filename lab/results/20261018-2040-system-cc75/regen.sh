#!/bin/sh
# Regen: rebuilds the patched tree and reflies the five rungs, then folds metrics.json.
# Patch: work/patch.diff (ES_LADDER scene knob + ES_SEEN_DUMP print-only census in the bench loop).
# Total ~4 min on 8 vCPU (build ~40 s; flights: <1 s, ~3 s, ~32 s, ~70 s, ~120 s).
set -e
cd "$(dirname "$0")/../../.."   # the repo root
R=$(pwd); W=$R/lab/results/20261018-2040-system-cc75/work
mkdir -p "$W"
git apply --allow-empty "$R/lab/results/20261018-2040-system-cc75/work/patch.diff" 2>/dev/null || true
cargo build --release -p xtask
T=$(cargo metadata --no-deps --format-version 1 | python3 -c "import json,sys; print(json.load(sys.stdin)['target_directory'])")/release/xtask
cd "$W"
ES_SEEN_DUMP=$W/seen0.txt      $T universe --bench --seed 1 --rtf 100 --seconds 2 --unpaced > bench0.json 2>&1
ES_LADDER=1000    ES_SEEN_DUMP=$W/seen1000.txt    $T universe --bench --seed 1 --rtf 100 --seconds 2 --unpaced > bench1000.json 2>&1
ES_LADDER=10000   ES_SEEN_DUMP=$W/seen10000.txt   $T universe --bench --seed 1 --rtf 100 --seconds 2 --unpaced > bench10000.json 2>&1
ES_LADDER=100000  ES_SEEN_DUMP=$W/seen100000.txt  $T universe --bench --seed 1 --rtf 100 --seconds 2 --unpaced > bench100000.json 2>&1
ES_LADDER=300000  ES_SEEN_DUMP=$W/seen300000.txt  $T universe --bench --seed 1 --rtf 100 --seconds 1 --unpaced > bench300000.json 2>&1
cd .. && python3 analyze.py > metrics.json && cat metrics.json
