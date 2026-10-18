#!/usr/bin/env bash
# Regenerates every number in dossier.md from the run's own scripts.
# ~80 s total. Deterministic except the price arm (order of magnitude only).
set -euo pipefail
cd "$(dirname "$0")"
python3 eclipse_parity.py
python3 analyze.py
