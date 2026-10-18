#!/bin/sh
# Regen: every number in dossier.md, from shipped code + work/patch.diff (applied by the runner
# before this runs). The patch adds scenario::{BeltDraw,belt_ship,plane_belt} (a pure refactor:
# plane_extra is bit-identical, proven by the CONTROL line) and examples/train.rs (the instrument).
# Total wall: warm build ~20 s + control ~4 s + 8 arms x ~55 s = ~8 min. Linux x86, release, < 2 GB.
set -e
cd "$(dirname "$0")/../../.."  # repo root
cd crates/universe
cargo run --release --example train 2>&1 | tee ../../lab/results/20261017-2330-second-20261017-2038-quant-b4a8-d520/raw-train.txt
python3 ../../lab/results/20261017-2330-second-20261017-2038-quant-b4a8-d520/rule.py < ../../lab/results/20261017-2330-second-20261017-2038-quant-b4a8-d520/raw-train.txt
