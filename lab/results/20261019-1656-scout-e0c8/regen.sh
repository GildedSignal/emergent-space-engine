#!/bin/sh
# Regenerates every number in dossier.md (the run-out.txt table) in ~2 s.
# No tree patch: this run edited no shipped code (float instrument + wiki page only).
cd "$(dirname "$0")"
python3 absorb.py 2>&1 | tee run-out.txt
