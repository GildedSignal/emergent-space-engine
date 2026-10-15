#!/bin/sh
# Regenerates every number in dossier.md from shipped code + work/patch.diff (applied by the
# runner before this runs). The patch = 3dc8's seam+demote-passages (applied verbatim from the
# run's own branch) + this run's census instrument (examples/arc_pin.rs, the mint-cause
# counters in bind.rs/universe.rs). Builds the example, freezes a private binary (a sibling
# rebuild of the shared target must not contaminate the flights), flies the depth matrix and
# the two smoke anchors. Total ≈ 11 min on the 8-vCPU box (build 1 min, matrix ≈ 10 min).
set -e
cd "$(dirname "$0")/../../.." || exit 1
R="$(pwd)/lab/results/20261015-1926-taleb-d6ba"

echo "== build =="
cargo build --release -p emergent-universe --example arc_pin

echo "== freeze a private binary (contamination defense) =="
BIN="$R/work/bin/arc_pin"
mkdir -p "$R/work/bin"
cp "${CARGO_TARGET_DIR:-$PWD/target}/release/examples/arc_pin" "$BIN"

mkdir -p "$R/flights"
echo "== the anchors (pre-wave smoke, cheap) =="
"$BIN" 10000 coast 5000 | tee "$R/flights/smoke_5k_ctl.txt" | grep -E "^arm|current-bindings|pinned_total"
ES_LAZY_ENTRY=1 ES_LAZY_PASSAGES=1 "$BIN" 10000 coast 5000 | tee "$R/flights/smoke_5k_var.txt" | grep -E "^arm|current-bindings|pinned_total"

echo "== the decisive depth matrix =="
sh "$R/matrix.sh" > "$R/regen-matrix.log" 2>&1 || true
tail -3 "$R/regen-matrix.log"
echo "REGEN DONE"
