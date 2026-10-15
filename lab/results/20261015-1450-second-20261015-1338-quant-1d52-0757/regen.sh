#!/bin/bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff (applied by
# the runner before this runs; applied here if the tree is clean). ~6 min on this 8-vCPU
# box: one build (~15 s warm / ~90 s cold) + 23 flights (one process at a time) + table.
set -u
cd "$(dirname "$0")"
ROOT=$(cd ../../.. && pwd)
if ! grep -q "HOT_RING" "$ROOT/crates/universe/src/bind.rs" 2>/dev/null; then
  git -C "$ROOT" apply "$PWD/work/patch.diff" || { echo "PATCH FAILED"; exit 1; }
fi
( cd "$ROOT/crates/universe" && cargo build --release --example lazy_flight 2>&1 | grep -E "^error" && exit 1 )
bash fly.sh | tee regen.log
