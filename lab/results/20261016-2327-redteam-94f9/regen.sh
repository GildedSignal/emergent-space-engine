#!/usr/bin/env bash
# Regenerates every number in dossier.md from the run's own script.
# Runtime: ~6 s. Requires python3 with numpy, scipy, mpmath (pip install if missing).
set -euo pipefail
cd "$(dirname "$0")"
python3 -c "import numpy, scipy, mpmath" 2>/dev/null || pip install --user numpy scipy mpmath
python3 work/flank.py | tee flank-out.txt
echo "=== regen complete; compare with dossier.md ==="
