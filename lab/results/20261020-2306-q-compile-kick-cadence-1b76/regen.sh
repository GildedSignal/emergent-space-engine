#!/usr/bin/env bash
# Regenerates every number in dossier.md for run 20261020-2306-q-compile-kick-cadence-1b76.
# This is a compile run: no shipped code is touched, work/patch.diff is absent by
# design (the tree outside lab/results/ was never edited), and every dossier number
# is a property of the two text artifacts: the page being compiled (lab/wiki/
# kick-cadence.md, untouched in the tree) and the compiled page (wiki/kick-cadence.md).
set -euo pipefail
cd "$(dirname "$0")"
[ -f work/patch.diff ] && [ -s work/patch.diff ] && echo "NOTE: work/patch.diff exists and is non-empty (unexpected for a compile run)" || true
python3 check_compile.py | tee regen-verify.log
