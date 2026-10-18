#!/usr/bin/env bash
# Regen: every dossier number, from the corrected compose_rung.py alone (its constants
# cite the shipped artifacts and the published gold-record constants; no tree edits were
# needed for this fix -- work/patch.diff is empty by design, the original run's numbers
# compose from the same constants). Runtime: < 1 s.
set -euo pipefail
cd "$(dirname "$0")"

echo "== the corrected 10^7-rung composition (dossier table, ~0.1 s) =="
python3 compose_rung.py > work/compose_out.txt
sed -n '/^arm/,$p' work/compose_out.txt

echo
echo "== the checker's named numbers regenerate =="
grep -q "1e9 add-back 0.097 s/s" work/compose_out.txt && echo "OK   stale-constant reading 0.097 (checker: 0.098)"
grep -q "honest 10^9 bar (5.99e6 gs): 0.548 s/s" work/compose_out.txt && echo "OK   e29c-bar reading 0.548 (checker: ~0.55)"
grep -q "N in \[3.17e+07, 5.50e+07\]" work/compose_out.txt && echo "OK   crossover [3.17e7, 5.50e7] (checker: 3.2-5.5e7)"
grep -q "  1.8-3.1 " work/compose_out.txt && echo "OK   1e8 wave 1.8-3.1x budget (checker: 1.8-3.1x)"
grep -q "fit error per bar 1e+05:+0.00%, 1e+06:-0.05%, 1e+09:+0.00%" work/compose_out.txt && echo "OK   T* N^-1/4 law reproduces e29c's three bars within 0.05%"
grep -q "212.6 ~= k\* 213" work/compose_out.txt && echo "OK   cadence x T*(1e9) = 212.6 ~= e29c's k* 213"

echo
echo "== constants trace to e29c's gold record (guarded; skip if branch absent) =="
if git show origin/claude/lab-20261017-2142-library-e29c:lab/results/20261017-2142-library-e29c/dossier.md > /tmp/e29c_dossier.md 2>/dev/null; then
  grep -q "5.99×10⁷ / 3.37×10⁷ / 5.99×10⁶" /tmp/e29c_dossier.md && echo "OK   T* bars 5.99e7/3.37e7/5.99e6 gs verbatim in e29c's dossier"
  grep -q "3.55×10⁻⁵ ev/B/gs" /tmp/e29c_dossier.md && echo "OK   cadence 3.55e-5 ev/B/gs verbatim in e29c's dossier"
  grep -q "0.6/213" /tmp/e29c_dossier.md && echo "OK   the 0.6/213 cost identity verbatim in e29c's dossier"
  git show origin/claude/lab-20261017-2142-library-e29c:lab/results/20261017-2142-library-e29c/bars.py 2>/dev/null | grep -q "REKICK_COST = 0.6" && echo "OK   REKICK_COST = 0.6 verbatim in e29c's bars.py (0.6 is a cost ratio, f5bd 0.51-0.6x)"
else
  echo "SKIP e29c branch not present in this clone (constants were copied verbatim; see compose_rung.py cites)"
fi

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo ../../../)"
grep -n "357 kicks a game-second = 36,000 a wall second" "$ROOT/artifacts/runs/nladder/ladder.txt" | head -1

echo
echo "REGEN DONE (exit 0)"
