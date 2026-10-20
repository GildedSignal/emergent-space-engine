#!/bin/sh
# Regenerates every number in dossier.md for run 20261020-2306-q-compile-memory-h-live-e208.
# Rebuilds wiki/memory-h-live.md from work/head.md + the live lab/wiki/memory-h-live.md
# (the over-budget original, restored by the runner before this runs) and re-verifies
# budgets, run-line and number preservation. Runtime: < 1 s.
cd "$(dirname "$0")" || exit 1
exec python3 work/compile_check.py
