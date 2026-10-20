#!/usr/bin/env bash
# Regen (b41f): every dossier number from shipped code + work/patch.diff (single copy,
# applies to a clean tree — c1ad's patch.diff defect fixed here). ~13 min on 8 vCPU.
# Patch = f1ca's exposure harness + stride gate + v4/v5 floor arms (c1ad) + v6 (this run:
# geometric pair-scan floors with death-horizon touch, verified-only base, coverage-aware
# cap_final). One binary; env selects the floor policy (v4/v5/v6, default v6).
set -uo pipefail
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261020-2102-second-20261020-2004-taleb-c1ad-b41f
mkdir -p $R/work/regen
if git apply --check $R/work/patch.diff 2>/dev/null; then git apply $R/work/patch.diff; else echo "(patch already applied)"; fi
cargo build --release --offline -p emergent-allocator --example exposure 1>&2
E=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-0}/release/examples/exposure
row() { grep '^done' "$1" 2>/dev/null | grep -oE 'present [0-9-]+' | awk '{print $2}'; }
arm() { case $1 in shipped) echo "0:";; v4) echo "1:ESE_FLOOR=v4";; v5) echo "1:ESE_FLOOR=v5";; v6) echo "1:ESE_FLOOR=v6";; esac; }

echo "== battle (seeds 11-21 odd x shipped/v4/v6; fire = exit 101 + FIRE lines) =="
for s in 11 13 15 17 19 21; do
  for a in shipped v4 v6; do
    IFS=: read G V <<< "$(arm $a)"; f=$R/work/regen/b_${a}_s${s}.err; rc=0
    env $V timeout 120 $E battle $s 2400 32 0 0.5 24 8704 4.5 $G >/dev/null 2>$f || rc=$?
    echo "battle $a s$s exit=$rc present=$(row $f) fires=$(grep -c FIRE $f || true)"
  done
done
echo "v6 battle equality law: $(cat $R/work/regen/b_v6_s*.err | grep -c '^RB') RB, m>0: $(cat $R/work/regen/b_v6_s*.err | grep '^RB' | grep -vc 'm=-\|m=0' || true), out!=[]: $(cat $R/work/regen/b_v6_s*.err | grep '^RB' | grep -vc 'out=\[\]' || true)"

echo "== family (clumps/mixed/streams/quiet, seeds 11/13 x shipped/v4/v5/v6) =="
for cls in clumps mixed streams quiet; do
  for s in 11 13; do
    for a in shipped v4 v5 v6; do
      IFS=: read G V <<< "$(arm $a)"; f=$R/work/regen/f_${cls}_${a}_s${s}.err; rc=0
      env $V timeout 90 $E $cls $s 600 32 0 2.0 12 4352 4.5 $G >/dev/null 2>$f || rc=$?
      echo "$cls $a s$s exit=$rc present=$(row $f) fires=$(grep -c FIRE $f || true)"
    done
  done
done
echo "v6 family equality law: $(cat $R/work/regen/f_*_v6_s*.err | grep -c '^RB') RB, m>0: $(cat $R/work/regen/f_*_v6_s*.err | grep '^RB' | grep -vc 'm=-\|m=0' || true), out!=[]: $(cat $R/work/regen/f_*_v6_s*.err | grep '^RB' | grep -vc 'out=\[\]' || true)"

echo "== crush (12 concurrent battle draws per arm) =="
for a in v6 v4; do
  IFS=: read G V <<< "$(arm $a)"
  for s in 11 13 15 17 19 21 23 25 27 29 31 33; do
    env $V timeout 300 $E battle $s 2400 32 0 0.5 24 8704 4.5 $G >/dev/null 2>$R/work/regen/c_${a}_s${s}.err &
  done
  wait
  echo "$a crush fires $(grep -l FIRE $R/work/regen/c_${a}_s*.err 2>/dev/null | wc -l)/12; present sorted: $(for f in $R/work/regen/c_${a}_s*.err; do row $f; done | sort -n | tr '\n' ' ')"
done
echo "v6 crush equality law: $(cat $R/work/regen/c_v6_s*.err | grep -c '^RB') RB, m>0: $(cat $R/work/regen/c_v6_s*.err | grep '^RB' | grep -vc 'm=-\|m=0' || true), out!=[]: $(cat $R/work/regen/c_v6_s*.err | grep '^RB' | grep -vc 'out=\[\]' || true)"
echo "v6 CAPGAP total: $(cat $R/work/regen/b_v6_s*.err $R/work/regen/f_*_v6_s*.err $R/work/regen/c_v6_s*.err | grep -c CAPGAP || true)"
echo done
