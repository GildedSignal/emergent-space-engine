#!/usr/bin/env bash
# Regenerates every dossier number from shipped code + work/patch.diff (= 23a6's bound +
# instrument patch, applies clean at 6db15364) + the committed predecessor artifacts
# (23a6's and a0a1's own branches, fetched into work/artifacts/). One flight (F1, the e3
# replica: 26 s wall, 1.45 GB peak) re-derives the per-answer series and the 1e5 ALL count;
# the 3e5/3e3 ALL legs stand on the committed artifacts (they exceed the 2-GB cap to re-fly).
# Total: build ~15 s + flight ~26 s + analysis ~1 s.
set -eu
RUN_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$RUN_DIR/../../.." && pwd)"
cd "$REPO"
cargo build --release -p emergent-universe --example nladder
BIN=${CARGO_TARGET_DIR:-target}/release/examples/nladder
cd "$RUN_DIR/work/flights"
ES_ANSWER_ANATOMY=1 ES_CARRY_BOUND=1 timeout 160 "$BIN" 100000 burn 25 1300 12 1 30000 \
  > f1_e3_replica.out 2> f1_e3_replica.err || true
cd "$RUN_DIR/work"
python3 analyze.py | tee analyze_out.txt
echo "regen done"
