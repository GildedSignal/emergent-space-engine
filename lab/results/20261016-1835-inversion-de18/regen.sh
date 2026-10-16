#!/usr/bin/env bash
# Regenerates every number in dossier.md. Runs AFTER work/patch.diff is applied
# (so lab/wiki.py is the patched one; the pristine copy is work/wiki-pristine.py).
# Nothing outside this run folder is written; total wall < 1 min.
set -uo pipefail
cd "$(dirname "$0")"
R=$(pwd)

ROOT=$(cd ../../.. && pwd)
echo "== P1: conflict growth in lab/wiki history (real publishes) =="
for page in nladder scan-queue encounters; do
  echo "-- $page.md"
  for c in $(git -C "$ROOT" log --format=%h -- "lab/wiki/$page.md" | head -8); do
    n=$(git -C "$ROOT" show "$c:lab/wiki/$page.md" 2>/dev/null | grep -c '^<<<<<<< ' || true)
    d=$(git -C "$ROOT" show "$c:lab/wiki/$page.md" 2>/dev/null | awk '/^<<<<<<< /{dd++; if(dd>m)m=dd} /^>>>>>>> /{dd--} END{print m+0}')
    echo "   $c markers=$n maxdepth=$d"
  done
done
echo "-- markers on the checked-out tree:"
grep -c '^<<<<<<< ' "$ROOT"/lab/wiki/*.md 2>/dev/null | grep -v ':0' || true
grep -n '<<<<<<<' "$ROOT/lab/wiki/index.md" || echo "   (index rows leak markers only inside table rows, not at line start)"
echo
echo "== P2-P4: shipped apply() on three concurrent same-section publishes (pristine) =="
bash work/replay-pristine.sh "$R/work/wiki-pristine.py" PRISTINE 2>&1 | grep '^\[PRISTINE\]'

echo
echo "== P5: the same sequence through the patched apply() =="
bash work/replay-pristine.sh "$R/../../wiki.py" PATCHED 2>&1 | grep '^\[PATCHED\]'

echo
echo "== P6: heal today's real pages on a copy; content preservation =="
ROOT=$(cd ../../.. && pwd)
python3 work/heal-check.py "$ROOT" 2>&1 | grep -vE '^wiki: healed'
