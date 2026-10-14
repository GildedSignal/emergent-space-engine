#!/usr/bin/env bash
# Regenerates every number in dossier.md from this folder's scripts.
# ~9 min: exact event search (3 spectra x 12k pairs, 6 workers) + controls + bench + ledger.
set -e
cd "$(dirname "$0")"
echo "== control: exact event search vs brute force (60 pairs) + checker-table spot check =="
python3 validate.py 2>&1 | tee gate2-out.txt
echo "--- sanity: the checker's per-da table, vector vs radial-only miss ---"
python3 sanity.py 2>&1 | tee -a gate2-out.txt
echo "== decisive: 3 spectra x 12k candidate pairs, exact Kepler misses + variants =="
python3 run_decisive.py
echo "== r bench: the wired gate's unit cost (scalar C) =="
cc -O2 -o bench_r bench_r.c -lm
./bench_r 2000000 | tee bench-r.txt
tee -a gate2-out.txt < bench-r.txt
echo "== ledger: gated = ungated x (surviving + f_r) on 1738's anchors =="
python3 ledger3.py | tee ledger3-out.txt
echo "done."
