#!/bin/bash
# Regenerates every number in dossier.md. ~10 min on this 8-vCPU box (first build cold).
# The tree patch (work/patch.diff = quant-1d52's seam+retention patch + this run's bounded
# rule `ES_RETAIN_MAX` + the inflight/sweep print) is applied by the runner before this
# runs; if the tree is clean instead, apply it here.
set -u
cd "$(dirname "$0")"
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo ../../..)
if ! grep -q "retain_bound_counters" "$ROOT/crates/universe/src/bind.rs" 2>/dev/null; then
  git -C "$ROOT" apply work/patch.diff || { echo "PATCH FAILED"; exit 1; }
fi
cd "$ROOT/crates/universe"
cargo build --release --example lazy_flight 2>&1 | grep -E "^error" && exit 1
BIN=""
for d in /home/glmlab/lab-target-*/release/examples/lazy_flight "$ROOT/target/release/examples/lazy_flight"; do
  [ -x "$d" ] && BIN="$d" && break
done
[ -z "$BIN" ] && { echo "NO BINARY"; exit 1; }

for spec in "100000 coast 48000 1" "10000 coast 20000 1" "10000 coast 20000 7"; do
  f=$(echo $spec | tr ' ' '_')
  env -u ES_LAZY_ENTRY -u ES_RETAIN -u ES_RETAIN_MAX "$BIN" $spec > ctl_$f.txt 2>&1
  env -u ES_RETAIN -u ES_RETAIN_MAX ES_LAZY_ENTRY=1 "$BIN" $spec > seam_$f.txt 2>&1
  env -u ES_RETAIN_MAX ES_LAZY_ENTRY=1 ES_RETAIN=1 "$BIN" $spec > retain_$f.txt 2>&1
  for S in 1024 4096 16384 65536; do
    ES_LAZY_ENTRY=1 ES_RETAIN=1 ES_RETAIN_MAX=$S "$BIN" $spec > bound${S}_$f.txt 2>&1
  done
done
# The sweep split (dossier: the miss bill is in flight) and the N-trend at matched cut.
ES_LAZY_ENTRY=1 ES_RETAIN=1 "$BIN" 100000 coast 48000 1 > sweep_retain_100000_coast_48000_1.txt 2>&1
ES_LAZY_ENTRY=1 ES_RETAIN=1 ES_RETAIN_MAX=4096 "$BIN" 100000 coast 48000 1 > sweep_bound4096_100000_coast_48000_1.txt 2>&1
for N in 100000 200000; do
  f=${N}_coast_20000_1
  ES_LAZY_ENTRY=1 ES_RETAIN=1 "$BIN" $N coast 20000 1 > retain_$f.txt 2>&1
  for S in 4096 16384; do
    ES_LAZY_ENTRY=1 ES_RETAIN=1 ES_RETAIN_MAX=$S "$BIN" $N coast 20000 1 > bound${S}_$f.txt 2>&1
  done
done
cd ..
python3 table.py
echo "REGEN DONE"
