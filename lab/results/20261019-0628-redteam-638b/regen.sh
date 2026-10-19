#!/bin/sh
# Regen for run 20261019-0628-redteam-638b (premise red-team: the strong-field view).
# Regenerates every number in dossier.md from the run's own instrument.
# Wall ~35 s, < 100 MB RSS. No repo code is needed (the oracle is the exact
# Schwarzschild null geodesic, cross-checked against the shipped gr_oracle's
# series and capture boundary in the controls block of results.json).
set -e
cd "$(dirname "$0")"
python3 sky.py
echo "regen done: results.json"
