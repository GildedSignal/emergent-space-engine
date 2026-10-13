#!/bin/sh
# Regenerates every number in dossier.md from this run's scripts.
# No patch needed: every edit of this run lives inside lab/results/20261013-2005-scout-d947/.
# Runtime ~20 s (falsifier ~10 s + probe <1 s + analysis <1 s), pure python3 stdlib.
cd "$(dirname "$0")"
python3 falsifier.py results.json
python3 probe_floor.py > probe_floor.txt
python3 analyze.py results.json > analysis.txt
echo "--- dossier tables (analysis.txt) ---"
cat analysis.txt
