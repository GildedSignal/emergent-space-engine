#!/usr/bin/env bash
# Regenerates every number in dossier.md/table.txt. No tree edits beyond this
# run folder (work/patch.diff is empty), ~1.1 s, python3 stdlib only.
set -euo pipefail
cd "$(dirname "$0")"
python3 contact_fix.py | tee table.txt
