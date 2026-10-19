#!/bin/sh
# Regen: every dossier number from this folder's script (no repo code touched;
# no patch.diff needed — this run edited no shipped file).
set -e
cd "$(dirname "$0")"
python3 falsifier.py
