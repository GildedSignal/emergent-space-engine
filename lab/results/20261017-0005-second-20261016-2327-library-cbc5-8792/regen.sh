#!/bin/bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff
# (0619's seam+retention+ring plus this run's print-only additions: demote timing,
#  ES_RETAIN_DWELL, the mid90 standing-resident snapshot). ~9 min on the 8-vCPU box:
# one build + 24 flights + the compose script.
set -u
cd "$(dirname "$0")"
ROOT=$(cd ../../.. && pwd)
TARGET=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-0}
if ! grep -q "ES_RETAIN_DWELL" "$ROOT/crates/universe/src/bind.rs" 2>/dev/null; then
  git -C "$ROOT" apply "$PWD/work/patch.diff" || { echo "PATCH FAILED"; exit 1; }
fi
( cd "$ROOT/crates/universe" && CARGO_TARGET_DIR="$TARGET" cargo build --release --example lazy_flight ) \
  || { echo "BUILD FAILED"; exit 1; }
mkdir -p bin && cp "$TARGET/release/examples/lazy_flight" bin/lazy_flight-8792
grep -aq ES_RETAIN_DWELL bin/lazy_flight-8792 || { echo "BINARY WITHOUT PATCH"; exit 1; }
sha256sum bin/lazy_flight-8792 | tee bin/binary.sha256
BIN="$PWD/bin/lazy_flight-8792" bash fly.sh | tee regen.log
python3 promo_ledger2.py | tee regen-table.txt
echo "== regen complete: compare regen-table.txt with ledger_out.txt (must be identical"
echo "   except wall_s/rss/promote p99/max timing noise; all counters and digests exact)"
