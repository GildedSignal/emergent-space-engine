#!/usr/bin/env bash
# Regenerates every number in dossier.md for run 20261014-2248-redteam-5cad.
# Total runtime ~2 min (each script < 60 s where possible; dwell_tail.py ~45 s,
# shadow_falsifier.py ~40 s). Float64, numpy; no repo build needed.
set -euo pipefail
cd "$(dirname "$0")"
python3 shadow_falsifier.py | tee shadow_out.txt
python3 dwell_tail.py | tee dwell_out.txt
echo "regen done"
