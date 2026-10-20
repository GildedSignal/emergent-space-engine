#!/usr/bin/env bash
# Regen for run 20261020-2306-second-20261020-2158-q-resolve-wiki-memory-2eb3-6ccc.
# Regenerates every dossier number from the repo, the run branches, this run's
# scripts and work/patch.diff (applied by the runner; applied here if not).
# Deterministic text work + git; well under 1 minute.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
RUN=lab/results/20261020-2306-second-20261020-2158-q-resolve-wiki-memory-2eb3-6ccc

# the publisher patch is the tree edit itself; apply it if the runner has not
grep -q "def fold_runs" lab/wiki.py || git apply "$RUN/work/patch.diff"
grep -q "def fold_runs" lab/wiki.py || { echo "patch not applied"; exit 1; }

# the pristine control is always regenerated from git (never trusted from work/)
git show HEAD:lab/wiki.py > "$RUN/work/wiki-pristine.py"
grep -q "def fold_runs" "$RUN/work/wiki-pristine.py" && { echo "control is not pristine"; exit 1; }

# 17/17 checks: S0 no-regression control, S1 the hand-merge, S2 the real publish
# replayed through the patched publisher, S3 idempotence, S4 the next publish with
# a corrected line, S5 the pristine-HEAD negative control, S6 the corpus ceiling.
python3 "$RUN/second_check.py"
