#!/bin/sh
# Fetches the shipped record of run 20261020-2306-q-compile-memory-h-live-e208:
# its own scripts and compiled page from its published branch, and the old page
# from the commit it started at (its `base` file). Nothing in lab/wiki is touched.
set -e
cd "$(dirname "$0")"
BR=origin/claude/lab-20261020-2306-q-compile-memory-h-live-e208
RES=lab/results/20261020-2306-q-compile-memory-h-live-e208
git show $BR:$RES/work/head.md          > head.md
git show $BR:$RES/work/compile_check.py > compile_check.py
git show $BR:$RES/wiki/memory-h-live.md > compiled-page.md
git show $BR:$RES/predictions.md        > e208-predictions.md
BASE=$(git show $BR:$RES/base)
echo "$BASE" > base
git show $BASE:lab/wiki/memory-h-live.md > old-page.md
echo "fetched: base=$BASE old-page $(wc -l < old-page.md) lines, compiled $(wc -l < compiled-page.md) lines, head $(wc -l < head.md) lines"
