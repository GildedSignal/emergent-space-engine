#!/usr/bin/env bash
# Regen for 20261021-0312-fermi-614b: every dossier number, from shipped code + this run's patch.
# ≤ 15 min: build ~15 s, eight arms ~90 s total on this machine.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
R=lab/results/20261021-0312-fermi-614b
if git apply --check "$R/work/patch.diff" 2>/dev/null; then git apply "$R/work/patch.diff"; fi
cargo build --release -p emergent-universe --example census
B="${CARGO_TARGET_DIR:-target}/release/examples/census"
test -x "$B" || { echo "no census binary" >&2; exit 1; }
cd "$R"
for a in "10000 coast 30 100 2 48 coast-s2-n1e4" "10000 burn 10 100 1 48 burn-s1-n10000" \
         "30000 burn 10 100 1 48 burn-s1-n30000" "100000 burn 10 100 1 48 burn-s1-n100000" \
         "300000 burn 10 100 1 48 burn-s1-n300000" "10000 burn 30 100 1 48 burn-s1-n10000-30s" \
         "0 burn 10 100 1 400 burn-s1-n0-m400" "10000 burn 10 100 1 400 burn-s1-n1e4-m400"; do
  set -- $a
  CENSUS_OUT="work/$6.json" "$B" "$1" "$2" "$3" "$4" "$5" "$7" >/dev/null
done
python3 work/analyze.py
