#!/bin/sh
# Regenerates every number in dossier.md from shipped code + work/patch.diff (applied by the
# runner before this runs). The patch is UNCHANGED from d6ba's (3dc8's seam+demote-passages
# verbatim + the census instrument) — verified by md5 against d6ba's published patch.
# Layout: build (~15 s) -> freeze a private binary -> the belt rows (serial, ~200 s) and the
# comet ladder (parallel: each flight is a single-threaded process; the critical path is the
# 48k arm ~700 s CPU) -> the summary greps. Total ~13-15 min on an idle 8-vCPU box; on a
# shared box the comet arms' wall time inflates with contention (their CPU need is fixed).
# The ctl comet arm peaks at rss ~2.8 GB (that is the point: shipped is ruin) — it runs last
# and best-effort so a box that kills >2 GB processes cannot poison the rest of the record.
set -e
cd "$(dirname "$0")/../../.." || exit 1
R="$(pwd)/lab/results/20261015-2041-second-20261015-1926-taleb-d6ba-57ec"

echo "== build =="
cargo build --release -p emergent-universe --example arc_pin

echo "== freeze a private binary (contamination defense) =="
BIN="$R/work/bin/arc_pin"
mkdir -p "$R/work/bin" "$R/flights"
cp "${CARGO_TARGET_DIR:-$PWD/target}/release/examples/arc_pin" "$BIN"

echo "== the matrix (belt serial, comet ladder parallel) =="
sh "$R/matrix.sh" > "$R/regen-matrix.log" 2>&1 || true
tail -4 "$R/regen-matrix.log"
echo "REGEN DONE"
