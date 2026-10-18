#!/bin/sh
# Regenerates every number in dossier.md (20261018-0035-redteam-22d1).
# Run from anywhere; ~10 s. Requires python3 with numpy.
set -e
cd "$(dirname "$0")"
python3 eclipse_parity.py
echo "---"
echo "Regen OK: compare eclipse_parity-out.json against the dossier's numbers."
