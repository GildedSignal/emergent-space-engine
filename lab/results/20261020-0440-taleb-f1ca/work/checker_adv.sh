#!/bin/bash
# Checker adversarial cases for f1ca. B is the patched exposure binary.
R=/home/glmlab/actions-runner/_work/emergent-space-engine/lab-1/lab/results/20261020-0440-taleb-f1ca
D=$R/work/cdraws
B=/home/glmlab/lab-target-1/release/examples/exposure
run() { local arm=$1 s=$2 blk=$3; local g=0; [ "$arm" != shipped ] && g=1
  local extra=""; [ "$arm" = v3 ] && extra="ESE_V3=1"
  env $extra "$B" battle "$s" 2400 32 8192 0.5 24 8704 4.5 "$g" 2>"$D/${blk}_${arm}_s$s.err" || echo "rc=$? ${blk}_${arm}_s$s" >> "$D/rc.txt"; }
echo "== A: fire hunt, shipped, fresh seeds 27-41 (sequential)"
for s in 27 29 31 33 35 37 39 41; do run shipped $s adv; done
echo "== B: scale 2x (galaxy 17408/48), s27 both arms (sequential)"
for arm in shipped v4; do s=$arm; g=0; [ "$s" != shipped ] && g=1
  "$B" battle 27 2400 32 8192 0.5 48 17408 4.5 "$g" 2>"$D/big_${arm}_s27.err" || echo "rc=$? big_${arm}_s27" >> "$D/rc.txt"; done
echo "== C: churn class (gas, rate 600, min_region 1), 2 seeds both arms (sequential)"
for s in 11 13; do for arm in shipped v4; do g=0; [ "$arm" != shipped ] && g=1
  "$B" gas "$s" 600 1 8192 0.5 12 4352 4.5 "$g" 2>"$D/gas_${arm}_s$s.err" || echo "rc=$? gas_${arm}_s$s" >> "$D/rc.txt"; done; done
echo "== D: duration 9s, s19 both arms (sequential)"
for arm in shipped v4; do g=0; [ "$arm" != shipped ] && g=1
  "$B" battle 19 2400 32 8192 0.5 24 8704 9.0 "$g" 2>"$D/long_${arm}_s19.err" || echo "rc=$? long_${arm}_s19" >> "$D/rc.txt"; done
echo "== E: 2-way concurrent s11 (the unmapped boundary)"
run shipped 11 two & run v4 11 two & wait
echo "== summary"
for f in "$D"/*.err; do a=$(basename "$f" .err)
  fire=$(grep -c FIRE "$f" || true)
  done=$(grep -m1 "^done" "$f" | grep -oE "present [0-9]+|rollbacks [0-9]+|final lead max [0-9]+" | tr '\n' ' ')
  echo "$a fire=$fire $done"; done | sort
grep -h FIRE "$D"/*.err || echo "no fires"
