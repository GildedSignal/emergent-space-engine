#!/bin/sh
# regen.sh — 20261018-2155-scout-9fd1. Regenerates every dossier number from the
# shipped tree (no patches needed; the toy is self-contained numpy).
set -e
cd "$(dirname "$0")"
python3 epoch_knee.py epoch_knee.csv
echo "--- dossier numbers check ---"
# controls: E=1 rows must be 0 leaks; noarm rows leak==hits
awk -F, '$1=="E1" && $5!=0 {print "P1 FAIL", $0; exit 1}' epoch_knee.csv
awk -F, '$1=="noarm" && $5!=$6 {print "P2 FAIL", $0; exit 1}' epoch_knee.csv
awk -F, '$1=="grid" && $2==0.08 && $3==512 {printf "E=512 kappa=0.08 leak/kick %s (dossier: 5.4e-6)\n", $8}' epoch_knee.csv
echo OK
