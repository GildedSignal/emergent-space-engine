#!/usr/bin/env bash
# 51ea: regenerate every dossier number from shipped code + work/patch.diff. ~4 min.
set -euo pipefail
cd "$(dirname "$0")/../../.."
RUN=lab/results/20261020-1326-fermi-51ea
git apply --3way "$RUN/work/patch.diff" 2>/dev/null || git apply "$RUN/work/patch.diff" || true
cargo build --release -p emergent-universe --example nladder
BIN="${CARGO_TARGET_DIR:-target}/release/examples/nladder"
cd "$RUN/work"
for arm in "100000 burn 40 400 d1b" "100000 coast 40 400 d2" "30000 burn 40 400 d3" "100000 burn 55 400 d4_1e5_burn_era2"; do
  set -- $arm
  ES_SCAN_TRACE=1 timeout 90 "$BIN" "$1" "$2" "$3" "$4" > "$5.log" 2>&1 || true
done
python3 analyze.py
