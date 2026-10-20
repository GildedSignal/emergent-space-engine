#!/bin/sh
# Regenerates every dossier number from the clean tree: applies the instrument patch (8994's
# alloc_scope + the ES_SEED knob), builds, flies the five arms, prints the analysis.
# ~3 min warm (build 15-120 s + 5 x 18 s flights + analysis); each flight < 100 MB RSS.
set -e
D=$(dirname "$0")
while [ "$D" != / ] && [ ! -f "$D/Cargo.toml" ]; do D=$D/..; done
cd "$D" || exit 1
[ -f Cargo.toml ] || { echo "FATAL: repo root not found" >&2; exit 1; }
R=lab/results/20261020-1621-fermi-5f76
if git apply --check "$R/work/patch.diff" 2>/dev/null; then
  git apply "$R/work/patch.diff"
elif grep -q 'ES_SEED' crates/universe/examples/alloc_scope.rs 2>/dev/null; then
  echo "patch already applied; continuing"
else
  echo "FATAL: patch neither applies nor is applied" >&2; exit 1
fi
mkdir -p /tmp/fermi5f76
cargo build --release -p emergent-universe --example alloc_scope 2>&1 | tail -2 > /tmp/fermi5f76-build.log
B=$(cargo metadata --format-version 1 --no-deps 2>/dev/null | tr ',' '\n' | grep -o '"target_directory":"[^"]*"' | cut -d'"' -f4)/release/examples
ES_ALLOC_SCOPE=1 ES_ALLOC_CSV=/tmp/fermi5f76/A1.csv "$B/alloc_scope" 10000 coast 30 2000 12 > /tmp/fermi5f76/A1.log 2>&1
ES_ALLOC_SCOPE=1 ES_SEED=2 ES_ALLOC_CSV=/tmp/fermi5f76/A2.csv "$B/alloc_scope" 10000 coast 30 2000 12 > /tmp/fermi5f76/A2.log 2>&1
ES_ALLOC_SCOPE=1 ES_SEED=3 ES_ALLOC_CSV=/tmp/fermi5f76/A3.csv "$B/alloc_scope" 10000 coast 30 2000 12 > /tmp/fermi5f76/A3.log 2>&1
ES_ALLOC_SCOPE=1 ES_SEED=2 ES_ALLOC_CSV=/tmp/fermi5f76/A4.csv "$B/alloc_scope" 30000 coast 30 2000 12 > /tmp/fermi5f76/A4.log 2>&1
ES_ALLOC_SCOPE=1 ES_SEED=2 ES_ALLOC_CSV=/tmp/fermi5f76/A5.csv "$B/alloc_scope" 100000 coast 30 2000 12 > /tmp/fermi5f76/A5.log 2>&1
echo "=== five arms flown; analysis:"
python3 "$R/analyze.py" /tmp/fermi5f76
echo "=== compare with dossier.md's table (A1..A5 rows)"
