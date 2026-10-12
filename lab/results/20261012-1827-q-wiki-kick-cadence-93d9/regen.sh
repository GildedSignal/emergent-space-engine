#!/bin/sh
# Regen for 20261012-1827-q-wiki-kick-cadence-93d9 (compiler run).
# Re-verifies every grade and every number quoted in wiki/kick-cadence.md and
# dossier.md against the published run branches. No simulation is regenerated:
# this run compiles runs; its numbers are the runs' own numbers.
# Runtime: ~30 s (git show + regex only).
set -e
cd "$(dirname "$0")/../../.."   # repo root
if [ -f lab/results/20261012-1827-q-wiki-kick-cadence-93d9/work/patch.diff ] && [ -s lab/results/20261012-1827-q-wiki-kick-cadence-93d9/work/patch.diff ]; then
  git apply lab/results/20261012-1827-q-wiki-kick-cadence-93d9/work/patch.diff
fi
exec python3 lab/results/20261012-1827-q-wiki-kick-cadence-93d9/check_compile.py
