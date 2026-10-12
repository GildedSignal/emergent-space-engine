#!/usr/bin/env bash
# regen.sh — regenerates every number in the dossier of
# 20261012-1904-q-wiki-b12-statistic-838c from the run branches (read-only, ~20 s).
# 1. verify.sh: 49 mechanical checks — the grades (P1), the ten sampled claims (P2),
#    the classification (P3). 2. The branch scan that found the missed B12 run.
# 3. The page-mechanics facts (header fields, verbatim 1715 line).
set -e
here="$(cd "$(dirname "$0")" && pwd)"
root="$(cd "$here/../../.." && pwd)"

echo "=== 1. grades, sampled claims, classification ==="
bash "$here/verify.sh"

echo
echo "=== 2. the 4-7 Oct B12 scan (finds q-plane-judge-65fd) ==="
cd "$root"
for b in $(git for-each-ref refs/remotes/origin/claude/lab-* --format='%(refname:short)' | sed 's|origin/claude/lab-||' | grep -E '^2026100[4-7]'); do
  n=$(git show "origin/claude/lab-$b:lab/results/$b/check.md" 2>/dev/null | grep -c "B12" || true)
  d=$(git show "origin/claude/lab-$b:lab/results/$b/dossier.md" 2>/dev/null | grep -c "B12" || true)
  if [ "${n:-0}" -gt 2 ] || [ "${d:-0}" -gt 4 ]; then echo "$b check:$n dossier:$d"; fi
done
echo
echo "=== 3. page mechanics ==="
p="$here/wiki/b12-statistic.md"
head -5 "$p"
echo "section headers (want 5): $(grep -c '^## ' "$p")"
grep -qF -- "- 20261012-1715-redteam-b12-v2-5dcb (red-team, pending grade): the v2 pooled statistic passes a minority leak at the declared rate; null miscalibrated; affine assumption measured; platform-noise at the cutoff." "$p" && echo "1715 line verbatim: yes"
echo "run lines (want 15): $(sed -n '/^## Runs/,$p' "$p" | grep -c '^- ')"
