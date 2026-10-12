#!/usr/bin/env bash
# Pull each run's checker abstract (check.md, first ~1200 chars) from its published branch.
set -u
cd "$(git rev-parse --show-toplevel)"
run=lab/results/20261012-1715-q-wiki-coorbital-cert-fd4f
out="$run/work/abstracts"
mkdir -p "$out"
: > "$out/all.md"
while read -r id; do
  [ -z "$id" ] && continue
  {
    echo "### $id"
    if git show "origin/claude/lab-$id:lab/results/$id/check.md" 2>/dev/null | cut -c1-1200; then
      :
    else
      echo "(no check.md on branch)"
    fi
    echo
  } >> "$out/all.md"
done < "$run/work/runs-all.txt"
wc -l "$out/all.md"
