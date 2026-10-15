#!/usr/bin/env bash
# Regen: rebuilds every number in dossier.md from shipped code + this run's probe
# (xtask/src/behave/trojan.rs, applied by the runner as work/patch.diff) in ~10 min.
set -euo pipefail
cd "$(dirname "$0")"/../../.. || exit 1  # repo root (this file: lab/results/<run>/regen.sh)
R="$(pwd)/lab/results/20261015-0128-dynamics-b9be"
cargo test --release -p xtask trojan_probe --no-run >/dev/null
for spec in "float-12 float 1e-12 7" "float-10 float 1e-10 7" "plane-7 plane 1 7" "plane-2 plane 1 2"; do
  set -- $spec
  TROJAN_OUT=$R/$1.jsonl TROJAN_ARM=$2 TROJAN_RTOL=$3 TROJAN_STEP=$4 TROJAN_PERIODS=512 TROJAN_WORKERS=8 \
    cargo test --release -p xtask trojan_probe -- --ignored --nocapture 2>&1 | grep "trojan:"
done
cd "$R" && python3 aggregate.py | tee aggregate.out
