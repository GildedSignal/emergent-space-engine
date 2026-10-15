#!/bin/bash
# Regenerates every number in dossier.md. ~6 min on this 8-vCPU box (2 build jobs).
# Arms per scene: ctl (shipped) / seam (ES_LAZY_ENTRY=1) / retain (ES_RETAIN=1, shared cache).
# The tree patch (work/patch.diff) must be applied by the runner before this runs; if the
# tree is clean instead, apply it here.
set -u
cd "$(dirname "$0")"
ROOT=../../..
if ! grep -q "RetainCache" $ROOT/crates/universe/src/bind.rs 2>/dev/null; then
  git -C $ROOT apply work/patch.diff || { echo "PATCH FAILED"; exit 1; }
fi
cd $ROOT/crates/universe && cargo build --release --example lazy_flight 2>&1 | grep -E "^error" && exit 1
BIN=/home/glmlab/lab-target-3/release/examples/lazy_flight
cd - >/dev/null
for scene in "10000 coast 20000 1" "10000 coast 20000 7" "100000 coast 20000 1" "100000 coast 48000 1"; do
  for arm in ctl seam retain; do
    case $arm in
      ctl)    env -u ES_LAZY_ENTRY -u ES_RETAIN $BIN $scene ;;
      seam)   env -u ES_RETAIN ES_LAZY_ENTRY=1 $BIN $scene ;;
      retain) ES_LAZY_ENTRY=1 ES_RETAIN=1 $BIN $scene ;;
    esac > flights/${arm}_$(echo $scene | tr ' ' '_').txt 2>&1
  done
done
python3 table.py
