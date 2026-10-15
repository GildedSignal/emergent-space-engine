#!/usr/bin/env bash
# Regenerates every dossier number from the shipped tree + work/patch.diff (applied first).
# ~4 minutes: 2 builds (~45 s), 8 lazyfly arms (~45 s), frame_digest pristine pair (~1 min).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
cd "$ROOT"
TD="${CARGO_TARGET_DIR:-/home/glmlab/lab-target-2}"
# 1. the seam (idempotent: skip if already applied)
if ! grep -q "pub enum EntrySlot" crates/universe/src/bind.rs; then
  git apply "$HERE/work/patch.diff"
fi
cargo build --release -p emergent-universe --example lazyfly --example frame_digest 2>&1 | grep -E "^error" -A8 || true
B="$TD/release/examples/lazyfly"
# 2. the eight arms (digest identity control vs ES_LAZY, canonical cut 16,000 game-s)
cd "$HERE/work"
run() { if [ "$2" = "lazy" ]; then ES_LAZY=1 "$B" "$3" "$4" "$5" 16000; else "$B" "$3" "$4" "$5" 16000; fi; }
run e4  ctrl 10000 1 coast | tee e4c.txt
run e4  lazy 10000 1 coast | tee e4l.txt
run e4b ctrl 10000 1 burn  | tee e4b_ctrl.txt
run e4b lazy 10000 1 burn  | tee e4b_lazy.txt
run s7  ctrl 10000 7 coast | tee s7_ctrl.txt
run s7  lazy 10000 7 coast | tee s7_lazy.txt
run e5  ctrl 100000 1 coast | tee e5_ctrl.txt
run e5  lazy 100000 1 coast | tee e5_lazy.txt
# 3. the pristine pair: patched tree gate-off vs clean tree, frame_digest's 8 scripted flights
F="$TD/release/examples/frame_digest"
"$F" 20 2>/dev/null | grep seed | awk -F'|' '{gsub(/ /,"",$2); print $2}' > patched_off.txt
git stash push -q -- crates 2>/dev/null || { git checkout -- crates/; }
cargo build --release -p emergent-universe --example frame_digest 2>&1 | grep -E "^error" -A8 || true
"$F" 20 2>/dev/null | grep seed | awk -F'|' '{gsub(/ /,"",$2); print $2}' > pristine.txt
if ! grep -q "pub enum EntrySlot" crates/universe/src/bind.rs; then
  git apply --exclude='*lazyfly*' "$HERE/work/patch.diff"
  cargo build --release -p emergent-universe --example lazyfly 2>&1 | grep -E "^error" -A8 || true
fi
echo "--- digest identity, control vs lazy (column 1 = digest) ---"
for p in e4 e4b s7 e5; do a=${p}_ctrl.txt; [ -f "$a" ] || a=e4c.txt; [ "$p" = e4 ] && a=e4c.txt; b=${p/e4b/e4b}; done
paste <(awk '{for(i=1;i<=NF;i++) if($i ~ /^digest=/) print substr($i,8)}' e4c.txt e4b_ctrl.txt s7_ctrl.txt e5_ctrl.txt) \
      <(awk '{for(i=1;i<=NF;i++) if($i ~ /^digest=/) print substr($i,8)}' e4l.txt e4b_lazy.txt s7_lazy.txt e5_lazy.txt) | awk '{print ($1==$2 ? "IDENTICAL " : "DIFFER "), $1}'
echo "--- pristine vs patched gate-off ---"
if diff -q pristine.txt patched_off.txt >/dev/null; then echo "PRISTINE_IDENTICAL (8 flights)"; else diff pristine.txt patched_off.txt; fi
