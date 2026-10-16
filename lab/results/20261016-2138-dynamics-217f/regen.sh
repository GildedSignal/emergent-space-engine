#!/bin/sh
# Regenerates every number in dossier.md from the shipped tree + work/patch.diff.
# Patch = the ratchet example (crates/allocator/examples/ratchet.rs) + the ES_DECAY arm
# (alloc.rs accept(); off = shipped verbatim). Each flight < 60 s on 8 vCPU.
set -e
RUN_DIR=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$RUN_DIR/../../.." && pwd)
cd "$ROOT"
# Apply the run's patch (skipped if already applied, so the script is idempotent).
git apply --check "$RUN_DIR/work/patch.diff" 2>/dev/null && git apply "$RUN_DIR/work/patch.diff"
cargo build -p emergent-allocator --release --offline --example ratchet
BIN=$(cargo build -p emergent-allocator --release --offline --example ratchet --message-format=json 2>/dev/null | jq -r 'select(.executable!=null)|.executable' | tail -1)
echo "== battery (Relativistic, shipped): quench, E frozen at 1 =="
"$BIN" battery 17 2000 1 2>/dev/null
echo "== batteryn (Newtonian, shipped): conflicts fire, ratchet latches =="
"$BIN" batteryn 17 2000 1 2>/dev/null
echo "== batteryn + ES_DECAY=1: bounded cycle, digest must equal the shipped arm's =="
ES_DECAY=1 "$BIN" batteryn 17 2000 1 2>/dev/null
echo "== batteryr (Relativistic near targets): zero conflicts at c-cap =="
"$BIN" batteryr 17 2000 1 2>/dev/null
echo "== OFF-arm identity: ES_DECAY=0 must be bit-identical to the shipped row set (compare digests by eye) =="
ES_DECAY=0 "$BIN" batteryn 17 2000 1 2>/dev/null
