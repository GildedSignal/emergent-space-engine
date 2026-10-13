#!/usr/bin/env bash
# Regenerates every number in dossier.md for run 20261013-0037-components-009b.
# The runner applies work/patch.diff (== fix-arm.patch here) before this runs; if not, it is
# re-applied below. One build carries both arms: ES_BASELINE_ARM=1 restores the shipped
# double compile at runtime. Budget: ~8 minutes cold.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../../.." && pwd)
cd "$REPO"
if ! grep -q "ES_BASELINE_ARM" crates/universe/src/bind.rs; then
  git apply "$HERE/fix-arm.patch"
fi
cp "$HERE/bind_probe.rs" crates/universe/examples/bind_probe.rs
cargo build --release -p emergent-universe --example bind_probe
BIN=$(cargo metadata --format-version 1 | jq -r .target_directory)/release/examples/bind_probe
for args in "600 48 1" "600 48 3" "600 400 1"; do
  ES_BASELINE_ARM=1 "$BIN" $args | grep -E "^bind calls|^digest" | sed "s/^/BASE /"
  "$BIN" $args | grep -E "^bind calls|^digest" | sed "s/^/FIX  /"
done | tee "$HERE/regen-ab.txt"
echo "--- digest comparison (must be three MATCH lines) ---"
grep ^BASE "$HERE/regen-ab.txt" | grep digest | awk '{print $3}' > "$HERE/.db"
grep ^FIX "$HERE/regen-ab.txt" | grep digest | awk '{print $3}' > "$HERE/.df"
paste "$HERE/.db" "$HERE/.df" | awk '{print ($1==$2 ? "DIGEST_MATCH" : "DIGEST_DIFF "$1" "$2)}'
rm -f "$HERE/.db" "$HERE/.df"
echo "--- suites (space + universe, release) ---"
cargo test --release -p emergent-space -p emergent-universe 2>&1 | grep -E "test result|FAILED" | tee "$HERE/regen-tests.txt"
