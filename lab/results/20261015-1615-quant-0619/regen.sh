#!/bin/bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff.
# ~11 min on the 8-vCPU box: one build (~15 s warm) + 21 flights + table.
# Lesson from 0757's checker: freeze a PRIVATE copy of the binary before flying,
# and prove it carries the patch (a sibling checkout may rebuild the shared target).
set -u
cd "$(dirname "$0")"
ROOT=$(cd ../../.. && pwd)
TARGET=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-0}
if ! grep -q "HOT_RING" "$ROOT/crates/universe/src/bind.rs" 2>/dev/null; then
  git -C "$ROOT" apply "$PWD/work/patch.diff" || { echo "PATCH FAILED"; exit 1; }
fi
( cd "$ROOT/crates/universe" && CARGO_TARGET_DIR="$TARGET" cargo build --release --example lazy_flight ) \
  || { echo "BUILD FAILED"; exit 1; }
mkdir -p bin && cp "$TARGET/release/examples/lazy_flight" bin/lazy_flight-0619
grep -aq ES_RETAIN_HOT bin/lazy_flight-0619 || { echo "BINARY WITHOUT PATCH"; exit 1; }
sha256sum bin/lazy_flight-0619 | tee bin/binary.sha256
bash knee.sh | tee regen.log
python3 knee_table.py | tee regen-table.txt
