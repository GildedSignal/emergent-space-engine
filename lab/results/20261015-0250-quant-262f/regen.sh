# regen.sh — regenerates every number in dossier.md
# No tree edits were made in this run (bench.py is standalone; work/patch.diff is empty).
# Wall ≈ 15 s + pip if missing.
set -e
cd "$(dirname "$0")"
python3 -c "import numpy, scipy" 2>/dev/null || pip install -q numpy scipy
python3 bench.py 2>&1 | grep -v Deprecation
