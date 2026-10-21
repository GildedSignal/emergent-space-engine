#!/usr/bin/env bash
# regen.sh — 20261021-0142-q-compile-budget-1e9-8179 (compile lens, wiki page budget-1e9).
# Regenerates every number in dossier.md from the shipped tree + this folder.
# The run edited no shipped file, so work/patch.diff is expected empty; it is
# applied only if present. Runtime: ~0.2 s.
set -euo pipefail
cd "$(dirname "$0")"
if [ -s work/patch.diff ]; then
  git -C "$(git rev-parse --show-toplevel 2>/dev/null || echo .)" apply --check work/patch.diff \
    && git -C "$(git rev-parse --show-toplevel 2>/dev/null || echo .)" apply work/patch.diff
  echo "regen: work/patch.diff applied"
else
  echo "regen: no tree patch (the compile touched only this results folder)"
fi
python3 audit.py | tee audit-out.txt
echo "regen: audit exit 0 — dossier numbers regenerated"
