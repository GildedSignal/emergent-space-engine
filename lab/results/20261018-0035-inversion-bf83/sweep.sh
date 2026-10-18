#!/bin/bash
# Exposure sweep: does the game's own scene shape fire the finality assert?
# One draw per process; panic => exit!=0 with "would revise its published tick".
EX=/home/glmlab/lab-target-3/release/examples/exposure
DIR=$(dirname "$0")
OUT=$DIR/sweep-results.txt
: > $OUT
run () { # arm seed rate min_region n margin
  local arm=$1 seed=$2 rate=$3 mr=$4 n=$5 m=$6 f=/tmp/draw_$$.txt
  timeout 90 $EX $arm $seed $rate $mr $n $m > $f 2>&1
  local code=$?
  local fire=no; grep -q "would revise its published tick" $f && fire=YES
  echo "arm=$arm seed=$seed rate=$rate mr=$mr n=$n margin=$m exit=$code fire=$fire :: $(grep -o 'present [0-9]*' $f | tail -1) $(grep -o 'rollbacks [0-9]*' $f | tail -1) $(grep -o 'final lead max [0-9]*' $f | tail -1)" >> $OUT
  [ $code -ne 0 ] && grep -m1 "would revise\|panicked" $f >> $OUT
}
for rep in 1 2; do
  for s in 11 13 15; do
    run clumps  $s 2400 1  0  0.5   # belt shape, churny knob
    run clumps  $s 2400 32 0  0.5   # belt shape, shipped knob
    run battle  $s 2400 32 0  0.5   # faction fleets
    run streams $s 2400 32 0  0.5   # cold crossing traffic
    run gas     $s 2400 1  512 0.5  # blob churn, no slack (churn control)
    run quiet   $s 2400 32 0  0.5   # negative control
  done
done
grep -c "fire=YES" $OUT; echo ---; grep "fire=" $OUT
