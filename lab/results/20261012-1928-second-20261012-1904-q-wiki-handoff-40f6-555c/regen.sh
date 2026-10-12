#!/usr/bin/env bash
# Regen for 20261012-1928-second-20261012-1904-q-wiki-handoff-40f6-555c
# (second-author run on the handoff wiki compile).
# A pure compile again: no engine/tree code is touched (work/patch.diff is
# empty by design), so every number in dossier.md and wiki/handoff.md is
# grounded in run records on the origin/claude/lab-* branches and in
# origin/main state. verify.py re-extracts and re-checks each needle
# (137 checks: the original 96 plus this run's 41), the window accounting
# (zero in-window hits unaccounted), and regenerates the two corrected
# counts live. ~20 s.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
RUN=lab/results/20261012-1928-second-20261012-1904-q-wiki-handoff-40f6-555c

if [ -f "$RUN/work/patch.diff" ]; then
  git apply --check "$RUN/work/patch.diff" 2>/dev/null && git apply "$RUN/work/patch.diff" || true
fi

python3 "$RUN/verify.py"

# Count (a), live: branches carrying a check.md — the denominator the
# original dossier misstated as "~200 run abstracts" (589 at its snapshot,
# 593 at this run's; branches keep landing).
n=0
git for-each-ref --format='%(refname:short)' refs/remotes/origin/claude/lab-\* | \
while read -r r; do
  if git cat-file -e "$r:lab/results/${r#origin/claude/lab-}/check.md" 2>/dev/null; then
    echo x
  fi
done | wc -l

# Count (b), live: the original run's own sweep regex over check.md
# abstracts (84 hits at this run's snapshot, 83 at the original's). Ids that
# appear live but not in the frozen snapshot landed after this run; they are
# listed as informational, not failures (the accounting is anchored at the
# snapshot by verify.py).
git for-each-ref --format='%(refname:short)' refs/remotes/origin/claude/lab-\* | \
while read -r r; do
  id=${r#origin/claude/lab-}
  if git show "$r:lab/results/$id/check.md" 2>/dev/null | head -c 2500 | \
     tr -cd '\11\12\15\40-\176' | grep -qiE 'handoff|doll boundary|between dolls'; then
    echo "$id"
  fi
done | sort > "$RUN/work/live-sweep.txt"
echo "live sweep: $(wc -l < "$RUN/work/live-sweep.txt") hits"
comm -13 <(sort "$RUN/work/sweep-hits.txt") "$RUN/work/live-sweep.txt" \
  | sed 's/^/post-snapshot (informational): /' || true
echo "regen done"
