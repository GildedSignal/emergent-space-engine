#!/usr/bin/env bash
# Regen (lab c1ad): every dossier number from shipped code + work/patch.diff.
# Patch = f1ca's arm (exposure harness + stride gate + v4 floor + instruments) + v5
# (per-region publish floors on both publish paths; merge-capping; ESE_FLOOR arms).
# ~4 min on 8 vCPU. Arms share one binary; env selects the floor policy.
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261020-2004-taleb-c1ad
mkdir -p $R/work/regen
git apply --check $R/work/patch.diff 2>/dev/null && git apply $R/work/patch.diff || echo "(patch already applied)"
cargo build --release --offline -p emergent-allocator --example exposure 1>&2
E=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-3}/release/examples/exposure

row() { grep '^done' "$1" 2>/dev/null | grep -oE 'present [0-9-]+' | awk '{print $2}'; }

echo "== battle protocol (8 seeds x 3 arms, one process per draw; fire = exit != 0) =="
for s in 11 13 15 17 19 21 23 25; do
  for arm in shipped v4 v5; do
    case $arm in shipped) G=0; V="";; v4) G=1; V="ESE_FLOOR=v4";; v5) G=1; V="ESE_FLOOR=v5";; esac
    rc=0; env $V timeout 120 $E battle $s 2400 32 0 0.5 24 8704 4.5 $G > /dev/null 2> $R/work/regen/b_${arm}_s${s}.err || rc=$?
    echo "$arm s$s exit=$rc present=$(row $R/work/regen/b_${arm}_s${s}.err) fires=$(grep -c FIRE $R/work/regen/b_${arm}_s${s}.err || true)"
  done
done
echo "equality law (v5 battle): $(cat $R/work/regen/b_v5_s*.err | grep -c '^RB') RB lines, m>0: $(cat $R/work/regen/b_v5_s*.err | grep '^RB' | grep -vc 'm=-\|m=0' || true), out!=[]: $(cat $R/work/regen/b_v5_s*.err | grep '^RB' | grep -vc 'out=\[\]' || true)"

echo "== crush (12 concurrent battle draws per arm, sequential blocks) =="
for arm in v5 v4 shipped; do
  case $arm in shipped) G=0; V="";; v4) G=1; V="ESE_FLOOR=v4";; v5) G=1; V="ESE_FLOOR=v5";; esac
  for s in 11 13 15 17 19 21 23 25 27 29 31 33; do
    env $V timeout 300 $E battle $s 2400 32 0 0.5 24 8704 4.5 $G > /dev/null 2> $R/work/regen/c_${arm}_s${s}.err &
  done
  wait
  echo "$arm crush fires $(grep -l FIRE $R/work/regen/c_${arm}_s*.err | wc -l)/12; present sorted: $(for f in $R/work/regen/c_${arm}_s*.err; do row $f; done | sort -n | tr '\n' ' ')"
done
echo "v5 crush equality law: $(cat $R/work/regen/c_v5_s*.err | grep -c '^RB') RB lines, m>0: $(cat $R/work/regen/c_v5_s*.err | grep '^RB' | grep -vc 'm=-\|m=0' || true), out!=[]: $(cat $R/work/regen/c_v5_s*.err | grep '^RB' | grep -vc 'out=\[\]' || true)"

echo "== quiet control (negative: 0 fires, 0 rollbacks in every arm) =="
for arm in shipped v5; do
  case $arm in shipped) G=0; V="";; v5) G=1; V="ESE_FLOOR=v5";; esac
  rc=0; env $V timeout 120 $E quiet 11 600 32 0 2.0 12 4352 4.5 $G > /dev/null 2> $R/work/regen/q_${arm}_s11.err || rc=$?
  echo "$arm exit=$rc present=$(row $R/work/regen/q_${arm}_s11.err) $(grep '^done' $R/work/regen/q_${arm}_s11.err | grep -oE 'rollbacks [0-9]+') fires=$(grep -c FIRE $R/work/regen/q_${arm}_s11.err || true)"
done
echo done
