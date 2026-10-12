#!/usr/bin/env bash
# Regen for 20261012-1715-q-wiki-memory-h-live-ef8a (wiki compiler run).
# Regenerates every number in dossier.md from the repo's lab run branches:
#   - the 111-run candidate set and each run's checker grade (check.md abstracts);
#   - the partition 82 memory-h-live + 24 off-topic + 5 ungraded (classify.py);
#   - the page's integrity: every cited id resolves, every Runs grade matches
#     its run's check.md, every claim <= 20 words (verify.py -> OK).
# No patch is needed (work/patch.diff is empty; this run edits nothing shipped).
# Runtime ~1 min. Run from the repo root (or anywhere: paths are self-locating).
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo="$(cd "$here/../../.." && pwd)"
cd "$repo"

# 1) re-extract the checker abstracts (first ~1100 bytes of each check.md)
mkdir -p "$here/work/abstracts"
while read -r id; do
  git show "origin/claude/lab-${id}:lab/results/${id}/check.md" 2>/dev/null \
    | head -c 1100 > "$here/work/abstracts/${id}.txt" || true
done < "$here/work/runs.txt"
n=$(find "$here/work/abstracts" -size +0c | wc -l)
echo "abstracts extracted: $n (expect 106 non-empty; 5 runs were never graded)"

# 2) partition check: 111 = 82 on-topic + 24 off-topic + 5 missing, no gaps
python3 "$here/work/classify.py"

# 3) page verification: ids, grades, claim lengths, partition
python3 "$here/work/verify.py"
