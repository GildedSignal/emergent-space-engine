#!/usr/bin/env bash
# Regenerates every number in dossier.md in ~1 s, from shipped code + work/patch.diff
# (the lab/wiki.py fold_runs patch; applied by the runner before this runs — the guard
# below makes it idempotent). No engine code is involved.
set -euo pipefail
cd "$(dirname "$0")/../../.."
MY=lab/results/20261021-0142-second-20261021-0106-q-compile-kick-jet-53a2-9141
if ! grep -q "def fold_runs" lab/wiki.py && [ -s "$MY/work/patch.diff" ]; then
  git apply "$MY/work/patch.diff"
fi
python3 "$MY/check_gold.py"
python3 "$MY/apply_demo.py"
