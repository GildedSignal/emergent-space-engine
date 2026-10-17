#!/bin/bash
# 20261017-2142-taleb-8fb9: regenerate every dossier number. The runner applies work/patch.diff first
# (scenario.rs's env-gated belt quantization + the belt_comb example). ~11 min on the lab box.
set -eu
cd "$(dirname "$0")/../../.."   # the repo root (work/patch.diff already applied)
cargo build --release -p emergent-universe --example belt_comb
cd lab/results/20261017-2142-taleb-8fb9
bash run_arms.sh work/arms
python3 analyze.py | tee work/arms/table.txt
echo "REGEN OK"
