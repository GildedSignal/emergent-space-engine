#!/usr/bin/env bash
# Regenenerates every number in dossier.md for run 20261019-2339-redteam-7bcf (r12-seen-flux).
# Runtime ~20 s. Outputs: metrics.json, diagnostics.json, run-output.txt, verdict.txt.
set -euo pipefail
cd "$(dirname "$0")"
python3 seen_flux.py > run-output.txt 2>&1
python3 ../../verdict.py r12-seen-flux.md metrics.json | tee verdict.txt
sha256sum -c rung-freeze.sha256
