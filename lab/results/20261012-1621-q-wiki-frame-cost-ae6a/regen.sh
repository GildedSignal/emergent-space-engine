#!/usr/bin/env bash
# Regen: every number in the dossier, from the immutable run branches and the
# shipped code. ~6 min on an 8-vCPU box (build 60 s + four 10 s benches).
# The compile's only tree edit is the one-line --members clamp lift kept in
# work/patch.diff (the probe needs it; run.sh also saves/restores the tree).
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$(git rev-parse --show-toplevel)"

# 1. apply the run's tree edit (the one-line --members clamp lift), if not applied
if [ -s work/patch.diff ]; then
  if git -C "$ROOT" apply --check work/patch.diff; then
    git -C "$ROOT" apply work/patch.diff
    echo "[regen] applied work/patch.diff"
  else
    echo "[regen] work/patch.diff already applied or tree moved on"
  fi
else
  echo "[regen] work/patch.diff empty"
fi

# 2. re-extract the 68 checker abstracts from the branches (the raw sources)
mkdir -p work/abstracts
while read -r r; do
  git show "origin/claude/lab-$r:lab/results/$r/check.md" 2>/dev/null \
    | head -c 1600 > "work/abstracts/$r.txt" || true
done < work/runs.txt
echo "[regen] abstracts: $(ls work/abstracts | wc -l) files"

# 3. regenerate the compile numbers: grade tally (branches vs cluster list),
#    classification counts, page faithfulness (ids, grades, 20-word claims)
python3 work/verify.py

# 4. regenerate the probe numbers (dossier: worst-hitch table)
TDIR="${CARGO_TARGET_DIR:-/home/glmlab/lab-target-probe}"
CARGO_TARGET_DIR="$TDIR" cargo build --release -p xtask 2>&1 | tail -1
XTASK="$TDIR/release/xtask" bash work/probe.sh
