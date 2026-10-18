#!/usr/bin/env bash
# regen.sh — regenerates every number in the dossier. No patch needed (the run
# edited no shipped code: work/ holds the Readwise cache, not a diff).
set -e
cd "$(dirname "$0")"
echo "== Readwise cache (fresh fetch if READWISE_TOKEN set) =="
python3 fetch_readwise.py
echo "== composition =="
python3 compose_fix.py
echo "== quote verification =="
python3 verify_quotes.py
echo "REGEN: PASS"
