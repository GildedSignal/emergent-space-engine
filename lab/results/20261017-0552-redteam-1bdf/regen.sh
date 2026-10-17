#!/bin/sh
# Regenerates every number in dossier.md from the run's own script.
# No network, no crates build; sympy from the system (present on the run box).
set -e
cd "$(dirname "$0")"
python3 -c "import sympy" 2>/dev/null || pip install --quiet sympy
cd work && python3 eob2pn_flank.py
