#!/usr/bin/env bash
# Regenerates every number in dossier.md: the compile audit (line counts,
# budgets, run retention, sampled numbers) against the shipped wiki page.
# This run edits no shipped code; work/patch.diff is applied if the runner
# saved one, and nothing here depends on it.
set -euo pipefail
cd "$(dirname "$0")"
if [ -f work/patch.diff ] && [ -s work/patch.diff ]; then
  git apply --check work/patch.diff 2>/dev/null && git apply work/patch.diff \
    || echo "note: work/patch.diff present but not applicable (no shipped-code edits expected)"
fi
python3 verify.py
