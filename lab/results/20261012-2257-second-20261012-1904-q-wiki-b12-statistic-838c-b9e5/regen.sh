#!/usr/bin/env bash
# regen.sh — regenerates every number in the dossier of
# 20261012-2257-second-20261012-1904-q-wiki-b12-statistic-838c-b9e5 from the run branches
# (read-only) and the reproduction scripts in work/repro/. ~30 s.
# work/patch.diff (empty: no tree edits outside this folder) is applied by the runner, if present.
set -e
here="$(cd "$(dirname "$0")" && pwd)"

echo "=== 0. restore the two shipped probes from their run branches ==="
git show origin/claude/lab-20261011-1234-library-069c:lab/results/20261011-1234-library-069c/b12probe.py > "$here/work/repro/b12probe.py"
git show origin/claude/lab-20261010-1029-library-6cfc:lab/results/20261010-1029-library-6cfc/probe_b12stat.py > "$here/work/repro/probe_b12stat.py"

echo "=== 1. verify.sh: 131 mechanical checks ==="
echo "    grades (P1/P1b), sampled claims from the 23 source runs (P2a/P2b),"
echo "    shipped-probe re-runs (P4/P5), the independent detune reproduction (P6),"
echo "    the full-branch sweep and classification (P3), page mechanics (P2c)."
bash "$here/verify.sh"

echo
echo "=== 2. the fold's headline repro numbers (for the dossier) ==="
python3 "$here/work/repro/detune_repro.py"
