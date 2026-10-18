#!/bin/sh
# Regenerates every number in dossier.md. Patch (work/patch.diff) is empty: no
# source changes. Deterministic; runs in ~1 s.
set -e
cd "$(dirname "$0")"
python3 compose.py > compose.out
cat compose.out
