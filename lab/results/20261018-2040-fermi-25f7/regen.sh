#!/bin/sh
# Regenerates every number in dossier.md from the shipped tree + this run's patch.
# ~4 min on the lab box (build ~40 s once deps are warm, flights ~2.5 min).
set -e
cd "$(dirname "$0")/../../.."

# apply this run's patch (the vladder instrument) if the tree does not already carry it
if [ ! -f crates/universe/examples/vladder.rs ]; then
  git apply lab/results/20261018-2040-fermi-25f7/work/patch.diff
fi

cargo build --release -p emergent-universe --example vladder 2>&1 | tail -1

BIN="${CARGO_TARGET_DIR:-/home/glmlab/lab-target-1}/release/examples/vladder"
OUT=lab/results/20261018-2040-fermi-25f7/work/vladder.log
{
  uptime
  for n in 0 500 1000 2000 4000 8000; do "$BIN" $n view 8 100 12; done
  echo "--- blind controls ---"
  for n in 2000 8000; do "$BIN" $n blind 8 100 12; done
  uptime
} | tee "$OUT"
echo "done: $OUT"
