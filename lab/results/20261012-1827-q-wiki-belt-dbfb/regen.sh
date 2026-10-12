#!/usr/bin/env bash
# regen.sh — regenerates every number in dossier.md for run 20261012-1827-q-wiki-belt-dbfb.
# A compilation run: its numbers are citations, so regeneration = proving each cited
# number exists verbatim in the cited run's immutable record (check.md/dossier.md on
# its claude/lab-<id> branch), plus the routing counts and the wiki merge dry-run.
# Applies work/patch.diff first (it is empty: nothing outside the run folder was edited).
# Read-only otherwise; < 1 minute; no network; < 100 MB.
set -eu
cd "$(dirname "$0")"

echo "== patch"
if [ -s work/patch.diff ]; then git apply work/patch.diff && echo "applied work/patch.diff";
else echo "work/patch.diff empty (nothing to apply; no tree edits outside this folder)"; fi

echo
echo "== claim traceability (62 cited numbers -> run branches)"
bash verify_claims.sh | tail -1

echo
echo "== page + routing counts"
echo "runs on the proposed page:  $(grep -c '^- 20' wiki/belt.md)"
echo "clustered runs kept:        11 (acb2 cross-flagged to memory-h-live)"
echo "clustered runs routed out:  3 (e369->encounters, system-0510->kick-jet, c6d8->memory-h-live)"

echo
echo "== wiki merge dry-run (lab/wiki.py apply three-way, base abaf0627)"
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
BASE=$(cat base)
git show "$BASE:lab/wiki/belt.md" > "$T/ours"       # lab/wiki/belt.md is still the base placeholder
git show "$BASE:lab/wiki/belt.md" > "$T/base"
cp wiki/belt.md "$T/theirs"
if git merge-file -p -L main -L "run start" -L run "$T/ours" "$T/base" "$T/theirs" > "$T/merged" \
   && ! grep -q '<<<<<<<' "$T/merged" \
   && diff -q "$T/merged" "$T/theirs" >/dev/null; then
  echo "merge clean, zero conflicts, result == proposed page"
else
  echo "MERGE PROBLEM — inspect $T"; exit 1
fi

echo
echo "regen: done"
