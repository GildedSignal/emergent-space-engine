#!/usr/bin/env bash
# Reproduce the decisive ensemble (each command <= ~90 s on the lab host;
# ~12 belt processes at >1 GB each will not fit -- run with parallelism <= 3).
set -eu
cd "$(dirname "$0")"
# Controls (pristine schedule): ~30 s each
for s in 1 2 3; do
  python3 belt.py --N 512 --T 1500 --sig_e 0.015 --b 4e-3 --mu 3e-7 --seed $s --nokick --out A_ctl_s$s.json
done
# Feedback scan: ~30-85 s each
for mu in 3e-8 3e-7 2e-6; do
  for s in 1 2 3; do
    python3 belt.py --N 512 --T 1500 --sig_e 0.015 --b 4e-3 --mu $mu --seed $s --out A_mu${mu}_s${s}.json
  done
done
# Weak-coupling unlock probe (T=300): ~170 s each, >1 GB RAM (N=512 only;
# larger N at this sig_e/W needs sig_e << W to stay honest — see dossier)
for s in 1 2; do
  python3 belt.py --N 512 --T 300 --sig_e 0.015 --b 4e-3 --mu 1e-9 --seed $s --out B_N512_s${s}.json
done
# Formations: ~1 s each
for mu in 1e-11 1e-8; do
  for form in aligned random; do
    for s in 1 2 3; do
      python3 belt.py --N 32 --formation $form --mu $mu --T 3000 --seed $s --out C_${form}_mu${mu}_s${s}.json
    done
  done
done
python3 analyze.py
