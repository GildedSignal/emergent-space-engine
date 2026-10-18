#!/bin/bash
# Regen: rebuild the exposure example from the run's patch and rerun both sweeps.
# ~7 minutes. Prereq: work/patch.diff applied (the runner applies it before this runs).
set -u
cd "$(dirname "$0")/../../.."   # repo root
RUN=lab/results/20261018-0035-inversion-bf83
git apply --check "$RUN/work/patch.diff" 2>/dev/null && git apply "$RUN/work/patch.diff"
cargo build -p emergent-allocator --release --offline --example exposure || exit 1
EX=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-3}/release/examples/exposure
[ -x "$EX" ] || EX=target/release/examples/exposure
cd "$RUN"
: > regen-results.txt
run () { # arm seed rate min_region n margin tag
  timeout 90 $EX "$1" "$2" "$3" "$4" "$5" "$6" > /tmp/regen_draw.txt 2>&1
  local c=$? f=no
  grep -q "would revise its published tick" /tmp/regen_draw.txt && f=yes
  echo "arm=$1 seed=$2 rate=$3 mr=$4 margin=$6 exit=$c fire=$f :: $(grep -o 'present [0-9]*' /tmp/regen_draw.txt | tail -1) $(grep -o 'rollbacks [0-9]*' /tmp/regen_draw.txt | tail -1) $(grep -o 'final lead max [0-9]*' /tmp/regen_draw.txt | tail -1)" >> regen-results.txt
}
# Protocol sweep (the decisive table; fires are wall-clock races, counts may move).
for rep in 1 2; do for s in 11 13 15; do
  run clumps  $s 2400 1  0   0.5
  run clumps  $s 2400 32 0   0.5
  run battle  $s 2400 32 0   0.5
  run streams $s 2400 32 0   0.5
  run gas     $s 2400 1  512 0.5
  run quiet   $s 2400 32 0   0.5
done; done
# Battle incidence + the shipped-default margin arm.
for rep in 1 2; do for s in 11 12 14 16; do run battle $s 2400 32 0 0.5; done; done
for rep in 1 2; do for s in 11 13 15;     do run battle $s 2400 32 0 2.0; done; done
# Margin axis on the churn blob (one probe draw per margin).
for m in 0.0 0.5 2.0; do run gas 3 2400 1 512 $m; done
echo "=== tallies (fires are race-decided; the dossier's point estimate was 1/14 at margin 0.5) ==="
awk '{for(i=1;i<=NF;i++) if($i ~ /^arm=$/){}} /fire=yes/{y++} /fire=no/{n++} END{print "fires:",y+0," clean:",n+0}' regen-results.txt
grep "fire=yes" regen-results.txt
echo done
