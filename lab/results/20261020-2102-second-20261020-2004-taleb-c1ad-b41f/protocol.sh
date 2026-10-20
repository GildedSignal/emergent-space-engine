#!/usr/bin/env bash
# Decisive protocol (b41f): battle 6 seeds x 3 arms; family 4 classes x 2 seeds x 4 arms;
# crush 12-way x v6/v4; equality law from every v6 draw. ~12 min on 8 vCPU.
set -uo pipefail
cd "$(dirname "$0")/../../.."
R=lab/results/20261020-2102-second-20261020-2004-taleb-c1ad-b41f
mkdir -p $R/work/draws
E=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-0}/release/examples/exposure
arm() { case $1 in shipped) echo "0:";; v4) echo "1:ESE_FLOOR=v4";; v5) echo "1:ESE_FLOOR=v5";; v6) echo "1:ESE_FLOOR=v6";; esac; }
row() { grep '^done' "$1" 2>/dev/null | grep -oE 'present [0-9-]+' | awk '{print $2}'; }

echo "== battle (galaxy 8704/24, rate 2400, margin 0.5, seeds 11-21 odd; fire = exit 101) =="
for s in 11 13 15 17 19 21; do
  for a in shipped v4 v6; do
    IFS=: read G V <<< "$(arm $a)"; f=$R/work/draws/b_${a}_s${s}.err; rc=0
    env $V timeout 120 $E battle $s 2400 32 0 0.5 24 8704 4.5 $G >/dev/null 2>$f || rc=$?
    echo "battle $a s$s exit=$rc present=$(row $f) fires=$(grep -c FIRE $f || true)"
  done
done
echo "v6 battle equality law: $(cat $R/work/draws/b_v6_s*.err | grep -c '^RB') RB, m>0: $(cat $R/work/draws/b_v6_s*.err | grep '^RB' | grep -vc 'm=-\|m=0' || true), out!=[]: $(cat $R/work/draws/b_v6_s*.err | grep '^RB' | grep -vc 'out=\[\]' || true)"

echo "== family (rate 600, min_region 32; the checker's kill scenes) =="
for cls in clumps mixed streams quiet; do
  for s in 11 13; do
    for a in shipped v4 v5 v6; do
      IFS=: read G V <<< "$(arm $a)"; f=$R/work/draws/f_${cls}_${a}_s${s}.err; rc=0
      env $V timeout 90 $E $cls $s 600 32 0 2.0 12 4352 4.5 $G >/dev/null 2>$f || rc=$?
      echo "$cls $a s$s exit=$rc present=$(row $f) fires=$(grep -c FIRE $f || true)"
    done
  done
done
echo "v6 family equality law: $(cat $R/work/draws/f_*_v6_s*.err | grep -c '^RB') RB, m>0: $(cat $R/work/draws/f_*_v6_s*.err | grep '^RB' | grep -vc 'm=-\|m=0' || true), out!=[]: $(cat $R/work/draws/f_*_v6_s*.err | grep '^RB' | grep -vc 'out=\[\]' || true)"

echo "== crush (12 concurrent battle draws per arm, sequential blocks) =="
for a in v6 v4; do
  IFS=: read G V <<< "$(arm $a)"
  for s in 11 13 15 17 19 21 23 25 27 29 31 33; do
    env $V timeout 300 $E battle $s 2400 32 0 0.5 24 8704 4.5 $G >/dev/null 2>$R/work/draws/c_${a}_s${s}.err &
  done
  wait
  echo "$a crush fires $(grep -l FIRE $R/work/draws/c_${a}_s*.err 2>/dev/null | wc -l)/12; present sorted: $(for f in $R/work/draws/c_${a}_s*.err; do row $f; done | sort -n | tr '\n' ' ')"
done
echo "v6 crush equality law: $(cat $R/work/draws/c_v6_s*.err | grep -c '^RB') RB, m>0: $(cat $R/work/draws/c_v6_s*.err | grep '^RB' | grep -vc 'm=-\|m=0' || true), out!=[]: $(cat $R/work/draws/c_v6_s*.err | grep '^RB' | grep -vc 'out=\[\]' || true)"
echo "v6 capgap lines: $(cat $R/work/draws/*_v6_*.err $R/work/draws/c_v6_s*.err 2>/dev/null | grep -c CAPGAP || true)"
echo done
