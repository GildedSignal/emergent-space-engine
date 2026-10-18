#!/bin/sh
# Regenerates every number in dossier.md: results.json (the falsifier's full output).
# No repo patch: this run edited nothing outside lab/results/20261018-1433-redteam-915d/.
cd "$(dirname "$0")"
exec python3 falsifier.py
