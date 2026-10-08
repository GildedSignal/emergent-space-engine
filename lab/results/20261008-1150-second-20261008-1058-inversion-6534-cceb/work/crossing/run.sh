#!/bin/sh
# Second author on 20261008-1058-inversion-6534: the checker's named experiment.
# Stage 1 (anchors): the original record regenerates from this tree (deterministic
# numbers identical to work/crossing-outputs.jsonl; only wall times drift, disclosed).
# Stage 2 (xcorr): the corridor in time — attribution redone.
# Stage 3 (xcert): the exit built — crossing-time-rank certificate, zero-miss vs
# truth at m >= 500, work per real encounter. Each step < 60 s on the cloud runner.
set -e
cd "$(dirname "$0")"
export CARGO_TARGET_DIR=/tmp/crossing-target
cargo build --release 2>&1 | tail -1
B=$CARGO_TARGET_DIR/release/crossing

echo "--- stage 1: anchors from the original record"
$B verify 100
$B cluster 500
$B block 500 ab
$B block 1000 ab

echo "--- stage 2: corridor attribution (distance to mean star vs own crossing; dt)"
$B xcorr 500 frozen
$B xcorr 500 steep
$B xcorr 500 tangent

echo "--- stage 3: the certificate (mean = checker's literal spec; own = per-body"
echo "    crossing; rank = conjunction-aware necessity window). truth=true => zero-miss"
echo "    vs dense truth over the full m^2 product."
$B xcert 500 mean frozen true
$B xcert 500 own frozen true
$B xcert 500 rank frozen true
$B xcert 1000 rank frozen true
$B xcert 2000 rank frozen false
$B xcert 500 rank steep true
$B xcert 500 rank tangent true
