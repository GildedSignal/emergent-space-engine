#!/bin/sh
# Regen: every number in dossier.md from the run's own scripts (numpy 1.26).
# ~7.5 min wall on the shared 8-vCPU box, peak RSS 1.23 GB (under the 2 GB cap).
# galprogram.py is be13's own module, unchanged (bugdemo/confirm2 import it).
cd "$(dirname "$0")"
set -e
python3 bugdemo.py   > bugdemo.out   2>&1     # ~1 s   (control C2 vs be13 bug 3)
python3 confirm2.py  > confirm2.out  2>&1     # ~7 min (the corrected dials)
echo "== bugdemo.out =="   && cat bugdemo.out
echo "== confirm2.out =="  && cat confirm2.out
