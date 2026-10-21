#!/usr/bin/env bash
# Regenerates every number in dossier.md, from shipped code (lab/wiki.py), this script's
# neighbour compile_check.py, the git branch heads, and work/patch.diff (applied by the
# runner before this runs; during the author's session the compiled page is already in
# lab/wiki/). Well under 1 minute; no build, no network beyond the local git object store.
set -uo pipefail
out=lab/results/20261021-0142-q-compile-cell-rebind-4c5b
{
  echo "== grades (branch heads) =="
  for r in 20261018-2312-system-9eeb 20261019-1316-components-ef8c \
           20261019-1316-system-f7c3 \
           20261019-1452-second-20261019-1316-system-f7c3-6e91; do
    printf '%s: ' "$r"; git log -1 --format=%s "origin/claude/lab-$r"
  done
  echo
  echo "== compile check: budgets (old and new), run lines, every number =="
  python3 "$out/compile_check.py"
  echo
  echo "== wiki.py index row on the compiled page (patch applied) =="
  python3 lab/wiki.py index
  grep -n "cell-rebind" lab/wiki/index.md
  git checkout -q -- lab/wiki/index.md   # leave the tree as the patch left it
} 2>&1 | tee "$out/regen.txt"
