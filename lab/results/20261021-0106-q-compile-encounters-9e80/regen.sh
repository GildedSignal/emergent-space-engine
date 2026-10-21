#!/bin/sh
# Regenerates every number in dossier.md for run 20261021-0106-q-compile-encounters-9e80.
# Baseline: the OLD page as committed at this run's base (file `base`); the compiled page
# is wiki/encounters.md in this folder. This run edits nothing outside its results folder,
# so work/patch.diff is empty and no patch needs applying. Runtime: < 5 s.
set -e
cd "$(dirname "$0")"
BASE=$(cat base)
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
if git -C "$ROOT" cat-file -e "$BASE:lab/wiki/encounters.md" 2>/dev/null; then
    git -C "$ROOT" show "$BASE:lab/wiki/encounters.md" > /tmp/encounters-old-$$.md
    OLD=/tmp/encounters-old-$$.md
else
    OLD="$ROOT/lab/wiki/encounters.md"   # fallback: the untouched tree page
fi
echo "== old page: $BASE:lab/wiki/encounters.md =="
python3 check_compile.py "$OLD"
rm -f "$OLD"
