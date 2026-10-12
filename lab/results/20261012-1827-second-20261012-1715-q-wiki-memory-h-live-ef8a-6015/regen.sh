#!/usr/bin/env bash
# Regen for 20261012-1827-second-20261012-1715-q-wiki-memory-h-live-ef8a-6015
# (second author on the memory-h-live wiki compile).
#
# Regenerates every number/claim in dossier.md from the repo's lab run branches:
#   1. the compiler run's 111-run cluster abstracts (copied verbatim from its
#      branch) + the 21 newly folded runs' abstracts (work/runs-added.txt);
#   2. the full-text sweep: every non-cluster branch's FULL dossier.md scanned
#      for memory-h-live markers; the discovery record work/sweep-hits.txt must
#      reproduce byte-identically (branches are immutable);
#   3. the partition of the 111 cluster runs (classify.py, unchanged);
#   4. the page's integrity (verify.py): 103 Runs lines = 82 cluster + 21 added,
#      every grade matches its run's check.md, every claim <= 20 words, every
#      cited id resolves, no added run compiled on another topic's page.
# No patch is needed (work/patch.diff is empty; this run edits nothing shipped).
# Runtime ~1 min. Run from anywhere: paths are self-locating.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo="$(cd "$here/../../.." && pwd)"
cd "$repo"

SRC=lab/results/20261012-1715-q-wiki-memory-h-live-ef8a
BR=origin/claude/lab-20261012-1715-q-wiki-memory-h-live-ef8a

# 1) abstracts: cluster (from the compiler run's branch) + the 21 added runs
mkdir -p "$here/work/abstracts"
git archive "$BR" "$SRC/work/abstracts" | tar -x -C /tmp
cp /tmp/$SRC/work/abstracts/*.txt "$here/work/abstracts/"
while read -r id; do
  git show "origin/claude/lab-${id}:lab/results/${id}/check.md" 2>/dev/null \
    | head -c 1100 > "$here/work/abstracts/${id}.txt" || true
done < "$here/work/runs-added.txt"
n=$(find "$here/work/abstracts" -size +0c | wc -l)
echo "abstracts non-empty: $n (expect 127 = 106 cluster + 21 added)"

# 2) full-text sweep reproduced; discovery record must be byte-identical
cp "$here/work/sweep-hits.txt" /tmp/sweep-hits.expected
python3 "$here/work/sweep.py" > /tmp/sweep-summary.txt
head -1 /tmp/sweep-summary.txt
cmp "$here/work/sweep-hits.txt" /tmp/sweep-hits.expected \
  && echo "sweep record reproduces byte-identically"

# 3) partition of the compiler's 111-run cluster (unchanged)
python3 "$here/work/classify.py"

# 4) page verification
python3 "$here/work/verify.py"
