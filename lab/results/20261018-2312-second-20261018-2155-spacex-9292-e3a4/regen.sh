#!/usr/bin/env bash
# Regenerates every number in dossier.md from the shipped tree + work/patch.diff (logs in work/).
# Arms: A (broken long window, 1e3 L15 1500 frames), C (10x-zoom window), A2 (1e4 L15, the K law
# and the belt fly-through), controls (coast; L8 interior at 1e4; seed 7).
# Total ~11 min on the shared 8-vCPU box; every process < 300 MB.
set -e
cd "$(git rev-parse --show-toplevel)"
R=lab/results/20261018-2312-second-20261018-2155-spacex-9292-e3a4
git apply "$R/work/patch.diff" 2>/dev/null || true
cargo build --release -p emergent-universe --example skyserve
B="$(cargo metadata --format-version 1 --no-deps | python3 -c 'import json,sys;print(json.load(sys.stdin)["target_directory"])')/release/examples/skyserve"
cd "$R/work"
"$B" 1000 burn 1500 100 1 15 0.008 60 1  > a1e3l15long.txt   # arm A: the checker's broken window
"$B" 1000 burn 360 100 1 15 0.0008 30 1  > c1e3l15zoom.txt   # arm C: the 10x-zoom window
"$B" 10000 burn 1500 100 1 15 0.008 420 1 > a2e4l15long.txt  # arm A2: K law + belt fly-through
"$B" 1000 coast 360 100 1 8 0.008 30 1   > ctl-coast.txt     # control: coast statics
"$B" 10000 burn 360 100 1 8 0.008 55 1   > ctl-l8.txt        # control: the interior window (9292's)
"$B" 10000 burn 360 100 1 8 0.008 55 7   > ctl-seed7.txt     # control: checker D (seed 7)
echo "regen done: grep 'anchors\|policy\|rebin\|near per frame\|never-repair\|raw angle' *.txt"
