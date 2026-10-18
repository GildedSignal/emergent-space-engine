#!/bin/sh
# Regen: every number in dossier.md from the run's own scripts (numpy 1.26).
# ~5 minutes wall on 8 vCPU, well under 2 GB (chunked sums; largest arrays
# are N x chunk float64 ~= 130 MB).
cd "$(dirname "$0")"
set -e
python3 galprogram.py > galprogram.out 2>&1
python3 confirm.py   > confirm.out 2>&1
echo "== galprogram.out (summary tail) ==" && tail -14 galprogram.out
echo "== confirm.out ==" && cat confirm.out
