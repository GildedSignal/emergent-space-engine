#!/usr/bin/env bash
# Regenerates every number in dossier.md from this run's scripts (no tree patch needed:
# the run edited no shipped code; work/patch.diff is absent/empty by construction).
set -euo pipefail
cd "$(dirname "$0")/work"
echo "== instrument self-test: static limit + FD vs analytic b1a =="
python3 news_strong.py
echo "== decisive grid (free-fall 4x4 + burns) =="
python3 sweep.py
echo "== pre-registered held-out rows =="
python3 sweep.py heldout
echo "== beta scan, burn/jerk scaling, RX completeness =="
python3 extra.py
echo "== done: sweep.json, sweep_heldout.json, scaling.json =="
