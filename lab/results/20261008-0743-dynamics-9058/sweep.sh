#!/bin/bash
# Sweep driver: cadence x flavor x lock-mode x scene. One CSV per run in data/.
set -u
cd "$(dirname "$0")"
mkdir -p data
A=0.3846
B=$(python3 -c "print(3**(-2/3))")
C=0.486
N=1000

run() { # name a e flavor K mode norbits
  local name=$1 a=$2 f=$3 k=$4 mode=$5 n=$6
  [ -s "data/$name.csv" ] || ./cadence "$a" 0.05 "$f" "$k" "$mode" "$n" > "data/$name.csv"
}
export -f run

jobs=()
for f in F W; do for mode in locked golden; do for k in 32 16 8 4 2 1 0.5 0.3; do
  jobs+=("run A-${f}-${k}-${mode} $A $f $k $mode $N")
done; done; done
for f in F W; do for mode in locked golden; do for k in 32 4 0.3; do
  jobs+=("run B-${f}-${k}-${mode} $B $f $k $mode $N")
  jobs+=("run C-${f}-${k}-${mode} $C $f $k $mode $N")
done; done; done
for f in F W; do for k in 0.997 0.99 0.97 0.9 0.7; do
  jobs+=("run D-${f}-${k} $A $f $k locked $N")
done; done
for f in F W; do for mode in locked golden; do for k in 32 1 0.3; do
  jobs+=("run L-${f}-${k}-${mode} $A $f $k $mode 10000")
done; done; done

printf '%s\n' "${jobs[@]}" | xargs -P 4 -I{} bash -c '{}'
echo "runs: $(ls data/*.csv | wc -l)"
