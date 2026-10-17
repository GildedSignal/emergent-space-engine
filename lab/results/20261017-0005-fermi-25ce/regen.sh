#!/bin/sh
# Regenerates every number in dossier.md for 20261017-0005-fermi-25ce.
# Total < 15 min; measured ~3 s. No network, no cargo build; python3 + numpy only.
set -e
cd "$(dirname "$0")"
python3 fermi_calendar.py | tee regen.out
echo "---"
echo "dossier tables: P3 forms + P4 ledger from '== P3'/'== P4'; P1 from '== P1';"
echo "P2 arms from '== P2'. Compare against dossier.md's Evidence section."
