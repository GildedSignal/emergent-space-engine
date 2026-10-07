#!/bin/bash
R=results.jsonl; : > $R
for dist in "6 26 wide" "10 14 narrow"; do
  set -- $dist; lo=$1; hi=$2; name=$3
  for N in 1000 100000 1000000 10000000 30000000; do
    case $N in 1000|100000|1000000) P=1000000;; 10000000) P=500000;; *) P=300000;; esac
    O=0; [ $N -le 10000 ] && O=1
    for s in heap2 heap4 wheel; do
      for seed in 11 29 47; do
        ./bench $s $N $lo $hi $seed $P $O >> $R
      done
    done
  done
done
