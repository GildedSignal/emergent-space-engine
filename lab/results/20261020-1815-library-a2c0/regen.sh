#!/usr/bin/env bash
# regen.sh — regenerates every dossier number. Read-only run: work/patch.diff is
# empty (no tree edits); everything below is fetched/derived fresh. ~40 s.
set -euo pipefail
cd "$(dirname "$0")"
echo "== patch check (read-only run: expect empty or absent) =="
if [ -s work/patch.diff ]; then wc -l work/patch.diff; else echo "empty/absent (read-only run, disclosed)"; fi
echo "== fresh Readwise export + quote verification (the held-out property) =="
python3 work/verify_quotes.py --fresh
echo "== the composition (every dossier number) =="
python3 work/compose.py | tee work/compose_out.txt
echo "== the five lessons =="
cat work/lessons.md
echo "== regen complete =="
