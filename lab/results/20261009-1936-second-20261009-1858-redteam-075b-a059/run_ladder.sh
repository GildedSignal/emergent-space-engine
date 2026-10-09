#!/bin/bash
# decisive ladder: e in {0.5,0.9}; s in {0.5,0.3,0.2,0.1,0.05,0.02,0.01}
cd "$(dirname "$0")"
run(){ # p e eps sign N floor seed tmode fd
  ./jet_anchor "$1" "$2" "$3" "$4" "$5" "$6" 1 "$7" 1e-3 32 "$8" "$9"
}
export -f run
jobs=()
for e in 0.5 0.9; do
  for s in 0.5 0.3 0.2 0.1 0.05 0.02 0.01; do
    p=$(python3 -c "print((6+2*$e)/(1-$s))")
    case $s in 0.5|0.3|0.2|0.1) N=300;; 0.05) N=200;; 0.02) N=150;; 0.01) N=100;; esac
    case $s in 0.02|0.01) fd=1e-4;; *) fd=1e-3;; esac
    for fl in 1e-6 1e-3; do for tm in 1 2; do for sd in 1 2; do
      echo "run $p $e 1e-4 0 $N $fl $sd $tm $fd"
    done; done; done
  done
done > ladder_jobs.txt
# extras: eps scaling + systematic
for s in 0.2 0.1 0.05; do p=$(python3 -c "print((6+2*0.9)/(1-$s))"); case $s in 0.05) N=200;; *) N=300;; esac
  for sd in 1 2; do echo "run $p 0.9 1e-5 0 $N 1e-6 $sd 1 1e-3"; done; done
for s in 0.1 0.05; do p=$(python3 -c "print((6+2*0.9)/(1-$s))"); case $s in 0.05) N=100;; *) N=100;; esac
  for tm in 1 2; do echo "run $p 0.9 1e-4 1 $N 1e-6 1 $tm 1e-3"; done; done
# convergence: h=5e-4 hot rung; fd=3e-3 vs 1e-3 H check via probes already banked
echo "run 8.2105 0.9 1e-4 0 200 1e-6 1 1 1e-3" >> ladder_jobs.txt
cat ladder_jobs.txt | xargs -P 7 -I{} bash -c '{}' > ladder.log 2>ladder.err
wc -l ladder.log
