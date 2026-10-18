#!/bin/sh
# Regenenerates every number in dossier.md from shipped code + work/patch.diff.
# ~3 minutes total on the lab's Linux x86 box (orders of magnitude only, per lab/README.md).
set -e
cd "$(dirname "$0")/../../.."   # the repo root (lab/results/<run> is three levels below it)

# The runner applies work/patch.diff before this script runs, so apply it ourselves only
# if it is present and not already in the tree (git apply --reverse --check succeeds then).
PATCH=lab/results/20261018-0431-components-25ef/work/patch.diff
if [ ! -s "$PATCH" ]; then
  grep -q A_WORD crates/universe/src/step.rs || { echo "no $PATCH and no arm in the tree"; exit 1; }
elif git apply --reverse --check "$PATCH" 2>/dev/null; then
  :  # already applied (the runner did it)
else
  git apply --check "$PATCH" && git apply "$PATCH"
fi
cd crates/universe
cargo build --release -q

echo "=== arm ON (A_WORD=2): the three frozen readout gates + the no-jump gate ==="
A_WORD=2 cargo test --release --test motion the_readout -- --nocapture 2>&1 \
  | grep -E "ship .*ramped readout|worst readout|judged|test result"

echo "=== arm OFF: the same gates, shipped per-read evaluation (bit-identical path) ==="
cargo test --release --test motion the_readout -- --nocapture 2>&1 \
  | grep -E "worst readout|judged|test result"

echo "=== arm ON: digests and outcomes (replay, memo, clock, origin) ==="
A_WORD=2 cargo test --release --test replay --test memo --test clock --test origin 2>&1 \
  | grep -E "running|test result|FAILED"

echo "=== arm ON: burns and flight (the clock re-plans under thrust; the word must re-arm) ==="
A_WORD=2 cargo test --release --test t1_burn --test p2_burn_out --test throttle 2>&1 \
  | grep -E "running|test result|FAILED"
