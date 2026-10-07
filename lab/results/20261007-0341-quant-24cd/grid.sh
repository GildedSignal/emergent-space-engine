#!/usr/bin/env bash
# The decisive grid for run 20261007-0341-quant-24cd. Sequential (timing on a shared machine).
# Usage: grid.sh <tag> <members> <rtf> <seconds> <engine_ms> <seed> [paced]
set -u
cd "$(dirname "$0")"
XT=/home/glmlab/lab-target-3/release/xtask
tag=$1; mem=$2; rtf=$3; secs=$4; ems=$5; seed=$6; paced=${7:-}
echo "== $tag members=$mem rtf=$rtf s=$secs engine_ms=$ems seed=$seed $paced $(date -u +%H:%M:%S) load=$(cut -d' ' -f1-3 /proc/loadavg)"
PLANE_FRAME_DUMP="frames-$tag.csv" timeout 120 "$XT" universe --bench --unpaced --members "$mem" --rtf "$rtf" --seconds "$secs" --engine-ms "$ems" --seed "$seed" $paced > "run-$tag.json" 2> "run-$tag.err" \
  || echo "  (exit $?; see run-$tag.err)"
python3 summary.py "$tag"
