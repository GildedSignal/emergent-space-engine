#!/bin/sh
# Regenerates every number in dossier.md from the run's own scripts.
# The record's baseline (the original run's instrument) is imported verbatim
# by path from orig-falsifier.py, which was taken unmodified from
# origin/claude/lab-20261017-2038-scout-8dfb.
# Wall time: ~10 s (21 rows x 30-dps quadrature + census + controls).
set -e
cd "$(dirname "$0")"
python3 port.py
