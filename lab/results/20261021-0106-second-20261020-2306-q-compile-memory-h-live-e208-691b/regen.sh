#!/bin/sh
# Regenerates every number in dossier.md for run
# 20261021-0106-second-20261020-2306-q-compile-memory-h-live-e208-691b.
# No tree edits outside this run folder are needed (work/patch.diff, if present,
# is empty of anything these scripts read). Total runtime: < 1 min.
#
#   fetch.sh         shipped record: e208's scripts+page from its published branch,
#                    the old 587-line page from its base commit 8a098f90
#   second_check.py  the missing second check, independent instruments (R0-R5)
#   section_local.py the named stronger instrument: section-local claim survival
#   mutation_test.py proves that instrument can fail (not a control)
#   cleanup.py       the proposed page (live 182 -> 179) + sandbox index dry-run
#                    + apply-union resurrection proof + three-way merge sim + P6
#   mod.rs grep      the +1 Refuted entry's code citation
set -e
cd "$(dirname "$0")"
sh work/fetch.sh
python3 work/second_check.py
python3 work/section_local.py
python3 work/mutation_test.py
python3 work/cleanup.py
echo "== code citation of the +1 Refuted entry =="
grep -n 'clamp(4, 400)' ../../../xtask/src/universe/mod.rs
echo "REGEN: ALL STEPS OK"
