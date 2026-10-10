#!/bin/sh
# Reproduces the run's numbers. Baseline binary: unmodified tree, `cargo build --release -p xtask`.
# Instrumented: this run's patch (lab/results/20261010-0920-quant-30e1/work/patch.diff).
B=${XTASK:-/home/glmlab/lab-target-3/release/xtask}
# per-kick budget, five seeds (digests 1/2/7 equal the unmodified build's):
for s in 1 11 23 2 7; do $B universe --kick-bench --seconds 10 --rtf 100 --members 400 --seed $s; done
# negative control (near-idle): counters stay ~0 outside kicks
$B universe --kick-bench --seconds 1 --rtf 1 --members 4 --seed 1
# whole-plane cross-check: engine vs view share, cost by kind
$B universe --bench --seconds 8 --rtf 100 --members 400 --unpaced --seed 1
