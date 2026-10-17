#!/usr/bin/env bash
# Regenerates every number in dossier.md. Total < 60 s (cached) / ~40 s + fetch.
set -euo pipefail
cd "$(dirname "$0")"
RUN=lab/results/20261017-1018-library-cf2a
[ -d "$RUN" ] || RUN=.
cd "$RUN"

# 1. Apply the run's tree patch if run.sh saved one (this run edited no
#    tracked files; the line is inert when the patch is absent).
if [ -f work/patch.diff ] && [ -s work/patch.diff ]; then
  git apply --check work/patch.diff 2>/dev/null && git apply work/patch.diff || true
fi

# 2. Readwise export: reuse the cache; refetch only if absent and token set.
if [ ! -f work/readwise_export.json ]; then
  python3 work/fetch_readwise.py
fi

# 3. Quote verification (dossier: "5/5 byte-identical").
python3 work/verify_quotes.py

# 4. The composition (dossier: P1 46.3/393.3/4,510.3 and 99.77%; P2 span
#    4.5e5-1.1e8; P3 49 < 1.6e3 deleted; P4 55 -> 7.4e6; P6 16x; rank 50x ->
#    0.7/7.7/90; lever ordering).
python3 work/compose_ledger.py
