#!/bin/sh
# Regenerates every number in dossier.md and verifies the five quotes.
# No tree edits were made by this run; work/patch.diff is applied if run.sh produced one.
cd "$(dirname "$0")"
if [ -f work/patch.diff ] && [ -s work/patch.diff ]; then
  git apply --check work/patch.diff 2>/dev/null && git apply work/patch.diff \
    && echo "applied work/patch.diff" || echo "patch.diff present but not applicable (tree may already carry it)"
fi
python3 work/promo_ledger.py
python3 work/quotes.py
