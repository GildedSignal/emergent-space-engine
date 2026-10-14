#!/bin/sh
# Regen (scout 29f4): every dossier number from shipped code + these scripts, <= 15 min.
# Applies nothing to the tree: copies the read-only example into the crate's examples dir,
# runs it (shipped pub APIs only), then the exact-rational analysis. Linux/x86, 1 thread.
set -e
cd "$(dirname "$0")"
ROOT=../../..
[ -f work_ikick.out ] || cp "$ROOT/crates/space/examples/ikick.rs" /tmp/ikick.shipped 2>/dev/null || true
cp ikick.rs "$ROOT/crates/space/examples/ikick.rs"
( cd "$ROOT" && cargo run --release -p emergent-space --example ikick ) > work_ikick.out 2>&1
rm -f "$ROOT/crates/space/examples/ikick.rs" /tmp/ikick.shipped
python3 analyze.py work_ikick.out > analysis.txt
grep -E "price cycle" work_ikick.out
echo "regen done"
