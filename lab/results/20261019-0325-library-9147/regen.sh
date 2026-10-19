#!/usr/bin/env bash
# Regenerates every number in dossier.md (~15 s). No patch is needed: the run edited no
# shipped file; work/patch.diff is absent/empty by construction (composition-only run).
set -euo pipefail
cd "$(dirname "$0")"
echo "== P1: five quotes byte-identical against a fresh Readwise export (falls back to the"
echo "   cached work/readwise.json if READWISE_TOKEN is unset) =="
python3 verify_quotes.py | tee work/verify_out.txt
echo
echo "== P2-P6: the composition (verdict arithmetic on page-cited constants + shipped code facts) =="
python3 compose_e9.py | tee work/compose_out.txt
echo
echo "Done. The dossier's table rows, the 9.15 TB median, the control regeneration, the"
echo "play-time laws and the code-fact counts (ship_ticks uses, child_ticks germ) are all above."
