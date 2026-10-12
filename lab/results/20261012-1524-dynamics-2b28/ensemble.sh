#!/usr/bin/env bash
# Decisive ensemble for run 20261012-1524-dynamics-2b28. Each command <= ~60 s.
set -u
cd "$(dirname "$0")"
CMDS=$(mktemp)
# A: belt feedback scan + controls
for mu in 1e-9 3e-8 3e-7 2e-6; do
  for s in 1 2 3; do
    echo "python3 belt.py --N 512 --T 1500 --sig_e 0.015 --b 4e-3 --mu $mu --seed $s --out A_mu${mu}_s${s}.json" >> "$CMDS"
  done
done
for s in 1 2 3; do
  echo "python3 belt.py --N 512 --T 1500 --sig_e 0.015 --b 4e-3 --mu 3e-7 --seed $s --nokick --out A_ctl_s${s}.json" >> "$CMDS"
done
# B: N scaling at fixed linear density (W proportional to N), weak coupling
for Nn in 512 1024 2048; do
  W=$(python3 -c "print($Nn*0.08/512)")
  for s in 1 2; do
    echo "python3 belt.py --N $Nn --W $W --T 300 --sig_e 0.015 --b 4e-3 --mu 1e-9 --seed $s --out B_N${Nn}_s${s}.json" >> "$CMDS"
  done
done
# C: formations, weak and strong coupling, aligned and random phases
for mu in 1e-11 1e-8; do
  for form in aligned random; do
    for s in 1 2 3; do
      echo "python3 belt.py --N 32 --formation $form --mu $mu --T 3000 --seed $s --out C_${form}_mu${mu}_s${s}.json" >> "$CMDS"
    done
  done
done
xargs -P 6 -a "$CMDS" -I{} -d'\n' sh -c '{}'
rm -f "$CMDS"
echo DONE
