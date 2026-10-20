#!/bin/sh
# Regenerates every number in dossier.md from shipped code + work/patch.diff (applied by the runner first).
# Total < 15 min: build ~10 s, four flights (26+48+36+20 s wall), analysis, fresh Readwise fetch ~8 s.
set -e
cd "$(dirname "$0")/../../.."   # run folder is <root>/lab/results/<id>: three levels up to the root
RUN=lab/results/20261020-0143-library-2d26
cargo build --release -p emergent-universe --example nladder
BIN="${CARGO_TARGET_DIR:-/home/glmlab/lab-target-3}/release"
cd "$RUN/work"
ES_FRAME_TRACE=f100000_burn.txt    "$BIN/examples/nladder" 100000 burn  18 2000 12 > out100000_burn.txt    2>&1
ES_FRAME_TRACE=f200000_burn.txt    "$BIN/examples/nladder" 200000 burn  18 2000 12 > out200000_burn.txt    2>&1
ES_FRAME_TRACE=f200000_burn400.txt "$BIN/examples/nladder" 200000 burn  46  400 12 > out200000_burn400.txt 2>&1
ES_FRAME_TRACE=f100000_coast.txt   "$BIN/examples/nladder" 100000 coast 18 2000 12 > out100000_coast.txt   2>&1
python3 analyze.py; python3 analyze400.py
python3 fetch_readwise.py readwise.json || echo "READWISE-REFRESH-FAILED: verifying against the cached export"
tail -n 1 out100000_burn.txt out200000_burn.txt out200000_burn400.txt out100000_coast.txt
