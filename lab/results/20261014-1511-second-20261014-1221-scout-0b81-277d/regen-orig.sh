#!/usr/bin/env bash
# Regenerates every number in dossier.md from this run's scripts.
# Runtime ~40 s (well under the 15-minute budget); needs python3 + numpy.
set -euo pipefail
cd "$(dirname "$0")"
python3 gate.py > gate-out.txt
python3 - << 'PYEOF' >> gate-out.txt
import gate
print("\n== part A (prediction 1): cell-pair worst case over phases ==")
print("  K sampled member-phase pairs -> min miss b at the crossing (vs 1/K)")
for K, b, inv in gate.phase_vacuity():
    print(f"  K={K:>7}: b_min = {b:.3e}  (1/K = {inv:.3e})")
PYEOF
cat gate-out.txt
