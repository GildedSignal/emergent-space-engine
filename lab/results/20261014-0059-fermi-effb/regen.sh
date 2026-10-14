#!/bin/sh
# Regenerates every number in the dossier from this folder (no network, no build).
# The code constants it reads are cited by file:line in ledger.py's header and were
# verified against this tree at commit 33c83f1a; the measured constants are cited to
# their wiki pages (gold runs listed there).
cd "$(dirname "$0")"
python3 ledger.py > ledger-out.txt
cat ledger-out.txt
