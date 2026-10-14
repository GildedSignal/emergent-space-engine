#!/bin/sh
# Regenerates every number in dossier.md from the patched tree (work/patch.diff is
# applied by the runner before this runs). ~1 min build + ~1 min runs on the lab box.
set -e
cd "$(dirname "$0")/../../../.."
BIN=$CARGO_TARGET_DIR/release/examples/impact_probe
echo "== build (patched tree) =="
cargo build --release -p emergent-universe --example impact_probe 2>&1 | tail -1
echo
echo "== OFF (the shipped path through the patched tree) =="
timeout 600 "$BIN"
echo
echo "== WARM (ES_IMP_WARM=1: the retired binding's impact tick as a verified seed) =="
ES_IMP_WARM=1 timeout 600 "$BIN"
echo
echo "== MODEL (ES_IMP_GUESS=1: the float Kepler inverse; the negative arm) =="
ES_IMP_GUESS=1 timeout 300 "$BIN" "battle m4000"
echo
echo "== identity =="
# One digest per arm per arm-set; diff them (field 4 of each arm line).
"$BIN" 2>/dev/null | grep -oE 'digest [0-9a-f]{16}' | awk '{print $2}' > /tmp/imp_off.txt
ES_IMP_WARM=1 "$BIN" 2>/dev/null | grep -oE 'digest [0-9a-f]{16}' | awk '{print $2}' > /tmp/imp_warm.txt
if diff -q /tmp/imp_off.txt /tmp/imp_warm.txt >/dev/null; then
  echo "PASS: every arm's digest is identical with the warm seed off and on ($(wc -l < /tmp/imp_off.txt) arms)"
else
  echo "FAIL: digests moved"; diff /tmp/imp_off.txt /tmp/imp_warm.txt; exit 1
fi
