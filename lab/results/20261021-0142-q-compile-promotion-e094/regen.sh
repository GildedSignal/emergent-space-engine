#!/bin/sh
# regen.sh — regenerates every number quoted in dossier.md for run
# 20261021-0142-q-compile-promotion-e094 (compile the `promotion` wiki page
# back under budget). No shipped code is rebuilt: this run's product is the
# compiled page wiki/promotion.md plus its verifier; every number below is a
# property of the two texts (the old page lab/wiki/promotion.md as restored by
# the runner, and this run's compiled page).
#
# Runtime: < 1 s. Requires python3 only.
set -e
cd "$(dirname "$0")"
echo "== verify.py (budgets, structure, runs, number census) =="
python3 verify.py
