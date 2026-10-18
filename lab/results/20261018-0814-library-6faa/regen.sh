#!/usr/bin/env bash
# Regenerates every number in dossier.md. No tree edits were needed for this run:
# work/patch.diff is applied only if present. Runtime: ~5 s offline.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

# Apply the run's tree edits (none for this run; keep the hook honest).
if [ -f work/patch.diff ] && [ -s work/patch.diff ]; then
  git apply --check work/patch.diff && git apply work/patch.diff
  echo "applied work/patch.diff"
else
  echo "no tree edits (work/patch.diff absent or empty)"
fi

python3 work/build_cache.py
python3 work/quotes.py
python3 work/ledger.py
