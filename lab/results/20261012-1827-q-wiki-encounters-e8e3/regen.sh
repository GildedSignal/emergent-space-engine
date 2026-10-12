#!/usr/bin/env bash
# Regen for 20261012-1827-q-wiki-encounters-e8e3 (compiler run, no new physics).
# The runner applies work/patch.diff before this script; nothing to build.
# Re-extracts the raw abstracts from the 65 refs, then re-derives the page's
# partition, grade tally, coorbital-cert disjointness and the sampled claims.
set -euo pipefail
cd "$(cd "$(dirname "$0")/../../.." && pwd)"
RUN=lab/results/20261012-1827-q-wiki-encounters-e8e3
python3 "$RUN/work/extract_abstracts.py"
python3 "$RUN/work/verify.py"
