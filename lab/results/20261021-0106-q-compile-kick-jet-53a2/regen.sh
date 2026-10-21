#!/usr/bin/env bash
# Regenerates every number in dossier.md (budget tallies, run-id census,
# number-faithfulness sweep) in ~0.1 s. No engine code is involved: the work
# is a wiki-page compile, so work/patch.diff carries no engine edits and
# nothing else needs rebuilding. The old page is read from lab/wiki/kick-jet.md
# (pristine tree), the compiled page from this run's wiki/kick-jet.md.
set -euo pipefail
cd "$(dirname "$0")/../../.."
exec python3 lab/results/20261021-0106-q-compile-kick-jet-53a2/check_compile.py
