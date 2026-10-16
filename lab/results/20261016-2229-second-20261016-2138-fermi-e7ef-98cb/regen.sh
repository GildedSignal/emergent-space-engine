#!/bin/bash
# Regenerates every number in dossier.md from the patched tree (the runner applies
# work/patch.diff before this runs). Total ~7 min on the lab box, < 1.5 GB per process.
set -eu
cd "$(dirname "$0")"
ROOT=../../..      # the repo root from lab/results/<run>
cd "$ROOT"

cargo build --release -p emergent-universe --example nladder --example belt_first 2>&1 | tail -1
BIN=$(cargo metadata --format-version 1 --no-deps | python3 -c "import json,sys; print(json.load(sys.stdin)['target_directory'])")/release/examples

cd - >/dev/null
export NL=$BIN/nladder BF=$BIN/belt_first
mkdir -p flights

echo "== the split's interval, direct (belt_first off/on)"
timeout 60 "$BF" 2>&1 | tail -2 > flights/belt_first-shipped.txt
BELT_SPLIT=1 timeout 60 "$BF" 2>&1 | tail -2 > flights/belt_first-split.txt
cat flights/belt_first-shipped.txt flights/belt_first-split.txt

echo "== the flight matrix"
./flights.sh

echo "== the ledger"
python3 ledger2.py
