#!/usr/bin/env bash
# Regenerates every number in dossier.md for run 20261020-1002-second-20261020-0440-redteam-9c08-870b
# (rung r13-sky-shift, frozen sha256 in rung-freeze.sha256). Runtime ~50 s, < 300 MB.
# Outputs: metrics.json, metrics-evidence.json, evidence.txt (author seed 20261020);
#          metrics-check.json, check-output.txt (fresh seed 31337); verdict.txt.
# The cell-struct read (struct-read.md) regenerates from the record's own branch, guarded below.
set -euo pipefail
cd "$(dirname "$0")"
python3 sky_shift.py > evidence.txt 2>&1
SKY_SEED=31337 METRICS_OUT=metrics-check.json python3 sky_shift.py > check-output.txt 2>&1
python3 ../../verdict.py r13-sky-shift.md metrics-check.json metrics.json | tee verdict.txt
sha256sum -c rung-freeze.sha256
grep -q "^Verdict: PASS" verdict.txt
PATCH=origin/claude/lab-20261019-0325-spacex-959a:lab/results/20261019-0325-spacex-959a/work/patch.diff
git show "$PATCH" | grep -q "e.lum += row.luminosity" \
  || { echo "struct read failed: the record's seen-flux sum line is gone"; exit 1; }
git show "$PATCH" | grep -q "luminosity: lum \* shift.powi(4)" \
  || { echo "struct read failed: the row's seen-flux line is gone"; exit 1; }
echo "struct read: CellSums seen-flux sum confirmed on the record's branch (959a)"
