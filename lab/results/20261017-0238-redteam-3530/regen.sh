#!/usr/bin/env bash
# Regenerates every number in dossier.md from this folder's scripts (~10 s, python3+numpy).
set -euo pipefail
cd "$(dirname "$0")"
python3 eob_flank.py controls
python3 decisive.py
echo "regen complete: controls must say PASS; tables reproduce dossier.md"
