#!/bin/sh
# Regenerates every number in dossier.md from shipped code plus work/patch.diff (applied by the
# runner before this runs). ~11 min total. Linux/x86: orders of magnitude only.
set -e
cd "$(dirname "$0")"
BIN=$(find /home/glmlab/lab-target-3 /target /tmp -maxdepth 6 -type f -name belt_floor -path "*release/examples*" 2>/dev/null | head -1)
if [ -z "$BIN" ]; then
  (cd ../../.. && cargo build --release -p emergent-universe --example belt_floor -j 6)
  BIN=$(find "$CARGO_TARGET_DIR" -type f -name belt_floor -path "*release/examples*" 2>/dev/null | head -1)
fi
echo "binary: $BIN"
mkdir -p data && cd data
# The ladder (seed 1, the ledger's own composition window), with per-body dumps.
for S in 7 5 3 1; do DUMP=1 TAG=s$S "$BIN" $S 267000 1 10000; done
# The locals probe and the held-out seed.
"$BIN" 3 267000 1 10000
"$BIN" 7 267000 7 10000
"$BIN" 1 267000 7 10000
# One full belt orbit at S=1 (boundedness of the drift).
DUMP=1 TAG=s1long "$BIN" 1 126000000 1 10000
cd ..
python3 analyze.py
