#!/usr/bin/env bash
# Regen for 20261012-1904-q-wiki-handoff-40f6 (compiler run).
# This run edits no engine/tree code (a pure wiki compile), so there is no
# work/patch.diff by design; every number in dossier.md and wiki/handoff.md is
# grounded in the run records on the origin/claude/lab-* branches, and
# verify.py re-extracts and re-checks each one against its source. ~15 s.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
RUN=lab/results/20261012-1904-q-wiki-handoff-40f6

if [ -f "$RUN/work/patch.diff" ]; then git apply --check "$RUN/work/patch.diff" && git apply "$RUN/work/patch.diff"; fi

python3 "$RUN/verify.py"

# The dossier's over-capture number: how many run abstracts mention the
# handoff/doll keywords (expect 83 on today's refs).
git for-each-ref --format='%(refname:short)' refs/remotes/origin/claude/lab-\* | \
while read -r r; do
  id=${r#origin/claude/lab-}
  if git show "$r:lab/results/$id/check.md" 2>/dev/null | head -c 2500 | \
     tr -cd '\11\12\15\40-\176' | grep -qiE 'handoff|doll boundary|between dolls'; then
    echo "$id"
  fi
done | wc -l
echo "regen done"
