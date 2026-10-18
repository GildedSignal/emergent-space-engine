#!/bin/sh
# Regen: every dossier number from the run's own script (float, ~3 s, numpy).
cd "$(dirname "$0")" && python3 falsifier.py > regen-out.txt 2>&1 && tail -32 regen-out.txt
