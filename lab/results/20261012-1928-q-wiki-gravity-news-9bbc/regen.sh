#!/usr/bin/env bash
# regen.sh — regenerates every number in the dossier and on the compiled page
# from the immutable run branches and the tree. Runtime: ~20 s (well under 15 min).
# This is a compile run: there is no experiment to rerun; the numbers are the
# runs' own recorded results, so "regenerate" = re-derive each quoted figure
# from its raw source (check.md / dossier.md on origin/claude/lab-<id>) and
# re-run the discovery sweep that fixed the run set.
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(git rev-parse --show-toplevel)
cd "$HERE"

# 0. The run's tree edits (none expected: all work lives in this folder).
if [ -s work/patch.diff ]; then git -C "$REPO" apply work/patch.diff; fi

# 1. Every quoted figure, re-derived from its branch (76 checks).
bash verify.sh

# 2. The discovery sweep: which runs belong to this topic.
git -C "$REPO" for-each-ref refs/remotes/origin/claude/lab-* --format='%(refname:short)' \
| while read -r r; do
    id=${r#origin/claude/lab-}
    out=$(git -C "$REPO" show "$r:lab/results/$id/check.md" 2>/dev/null | strings)
    m=$(printf '%s' "$out" | LC_ALL=C grep -m1 -aiE \
      'news (channel|gravity|at)|news-at-c|retarded news|version ring|gravity.{0,12}cursor|cursor.{0,12}news|octave accumulator|news-chain|news chain|b-news-gravity|gravity is news' || true)
    if [ -n "$m" ]; then echo "$id"; fi
  done | sort > work/sweep.txt
wc -l < work/sweep.txt
cat work/sweep.txt

# 3. The grades, re-read from each branch's check.md first line.
echo '--- grades ---'
for id in \
  20261005-1540-q-gravity-cursor-05b0 \
  20261006-1738-b-news-gravity-e300 \
  20261007-1918-scout-3da3 \
  20261007-2002-second-20261007-1918-scout-3da3-3fb7 \
  20261008-0148-system-098e \
  20261008-0234-second-20261008-0148-system-098e-bd06 \
  20261008-1859-scout-141c \
  20261008-1947-second-20261008-1859-scout-141c-3186 \
  20261009-0521-redteam-93a4 \
  20261009-0709-scout-5b6a \
  20261010-0814-system-fbc6 \
  20261010-0920-scout-e5f5 \
  20261010-0920-second-20261010-0814-system-fbc6-b903 \
  20261010-1029-second-20261010-0920-scout-e5f5-0c3b \
  20261010-1544-scout-c4cb; do
  g=$(git -C "$REPO" show "origin/claude/lab-$id:lab/results/$id/check.md" 2>/dev/null \
      | LC_ALL=C grep -m1 -aoE 'Grade: (gold|silver|lead|void)' || echo 'Grade: (none)')
  echo "$id :: $g"
done
echo '20261006-1931-second-20261006-1738-b-news-gravity-e300-e1ac :: Grade: (void — 429 at birth, no check.md, no dossier)'
echo '20261009-0621-second-20261009-0521-redteam-93a4-e93c :: Grade: (unchecked — checker 429; dossier + frozen rung r-news shipped)'

echo '--- done: PASS above means every dossier number regenerated ---'
