#!/bin/sh
# Regen for 20261012-1904-second-...-673b (second author on the kick-cadence page fold).
# Re-verifies every grade and every number quoted in wiki/kick-cadence.md and
# dossier.md against the published run branches, and re-derives the dossier's
# grade tally from the page itself. No simulation is regenerated: this run
# compiles runs; its numbers are the runs' own numbers.
# Runtime: ~40 s (git show + regex only).
set -e
cd "$(dirname "$0")/../../.."   # repo root
if [ -f lab/results/20261012-1904-second-20261012-1827-q-wiki-kick-cadence-93d9-673b/work/patch.diff ] && [ -s lab/results/20261012-1904-second-20261012-1827-q-wiki-kick-cadence-93d9-673b/work/patch.diff ]; then
  git apply lab/results/20261012-1904-second-20261012-1827-q-wiki-kick-cadence-93d9-673b/work/patch.diff
fi
exec python3 lab/results/20261012-1904-second-20261012-1827-q-wiki-kick-cadence-93d9-673b/check_compile.py
