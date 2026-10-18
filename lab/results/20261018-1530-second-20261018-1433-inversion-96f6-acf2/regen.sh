#!/bin/sh
# Regenerates every number in dossier.md from a restored tree: applies work/patch.diff
# (96f6's instrument verbatim — 7581's harness, deduplicated — PLUS this run's pin
# registry (Drop-counted distinct Arc<Scan> + bytes by capacity and by len), trigger
# census in same_inputs, per-frame pin log, and the native phase-compare bench), builds
# scanprobe, flies the K-trend, the three time-wall flights, and prints the tables.
# Deterministic columns (digests, kicks, events, census) must match 96f6's record at
# every K; the pin columns are this run's own. The 5e4 rows are deadline-coupled through
# game_s (mints follow the slid game_s) — orders of magnitude only there. ~3 min cold.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
P="$HERE/work/patch.diff"
cd "$HERE/../../.."   # repo root
if git apply --check --reverse "$P" 2>/dev/null; then
  echo "patch already applied; skipping"
elif git apply --check "$P" 2>/dev/null; then
  git apply "$P"
else
  git apply --3way "$P" || { echo "patch does not apply to this tree" >&2; exit 1; }
fi
cargo build --release --features prof -p emergent-universe --example scanprobe
B=${CARGO_TARGET_DIR:-target}/release/examples/scanprobe
OUT="$HERE/regen"; mkdir -p "$OUT"; cd "$OUT"
# the K-trend (composed = ES_SECULAR+ES_CHAIN+ES_LOCAL_STAGGER), 600 frames each
for k in 10000 20000 30000 50000; do
  rm -f pin-$k.txt
  env ES_SECULAR=1 ES_CHAIN=1 ES_LOCAL_STAGGER=1 ES_PIN=pin-$k.txt $B $k 0 10 100 > comp-$k.log 2>&1
done
# the time wall at fixed K: 1,200 / 1,200 / 2,400 frames (peak ~1.2 GB, inside the lab budget)
rm -f pin-50k-long.txt pin-30k-long.txt pin-10k-long.txt
env ES_SECULAR=1 ES_CHAIN=1 ES_LOCAL_STAGGER=1 ES_PIN=pin-50k-long.txt ES_WALL=110 $B 50000 0 20 100 > comp-50000-long.log 2>&1
env ES_SECULAR=1 ES_CHAIN=1 ES_LOCAL_STAGGER=1 ES_PIN=pin-30k-long.txt ES_WALL=110 $B 30000 0 20 100 > comp-30000-long.log 2>&1
env ES_SECULAR=1 ES_CHAIN=1 ES_LOCAL_STAGGER=1 ES_PIN=pin-10k-long.txt ES_WALL=110 $B 10000 0 40 100 > comp-10000-long.log 2>&1
python3 ../analyze.py .
echo "regen done: deterministic columns must equal 96f6's record; 5e4 rows deadline-coupled through game_s (disclosed)"
