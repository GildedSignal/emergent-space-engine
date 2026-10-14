#!/bin/sh
# Regenerates every number in the dossier (work/key_quantum.out) from this run's script.
# No patch is needed: the run edited nothing outside lab/results/ (work/patch.diff absent).
set -e
cd "$(dirname "$0")"
python3 key_quantum.py > work/key_quantum.regen.out 2>&1
echo "--- regen complete; diff against the dossier's run (empty = identical) ---"
if diff work/key_quantum.out work/key_quantum.regen.out; then echo "identical"; fi
