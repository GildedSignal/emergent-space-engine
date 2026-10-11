#!/bin/bash
# The decomposition grid: members x budget, coast, unpaced, 10 s, seed 1, series saved.
# Plus the paced worst cell, the original row-1 regeneration, and the default-scene budget sweep.
set -u
X=/home/glmlab/lab-target-0/release/xtask
cd "$(dirname "$0")"
D=data
run() { # name args...
  local name=$1; shift
  echo "== $name: $*"
  $X universe --bench --seed 1 --threads 1 "$@" > $D/$name.json 2>$D/$name.err || echo "FAILED $name"
}
# the grid
for M in 4 100 400; do
  for B in 5 1 0.2 0.05; do
    run "G-m${M}-b${B}" --rtf 3000 --seconds 10 --unpaced --coast --members $M --engine-ms $B --series $D/G-m${M}-b${B}.csv
  done
done
# default scene (members 48) budget sweep with series (regenerates the author's B row)
for B in 5 1 0.2 0.05; do
  run "B-b${B}" --rtf 3000 --seconds 10 --unpaced --coast --engine-ms $B --series $D/B-b${B}.csv
done
# the paced worst cell
run "P-m400-b0.2" --rtf 3000 --seconds 10 --coast --members 400 --engine-ms 0.2 --series $D/P-m400-b0.2.csv
run "P-m400-b5"   --rtf 3000 --seconds 10 --coast --members 400 --engine-ms 5   --series $D/P-m400-b5.csv
run "P-m4-b0.2"   --rtf 3000 --seconds 10 --coast --members 4   --engine-ms 0.2 --series $D/P-m4-b0.2.csv
# original row-1 regeneration: scripted (no coast) for 300/3000/30000, coast for 300000
run "R1-300-scripted"   --rtf 300   --seconds 10 --unpaced
run "R1-3000-scripted"  --rtf 3000  --seconds 10 --unpaced
run "R1-30000-scripted" --rtf 30000 --seconds 10 --unpaced
run "R1-300000-coast"   --rtf 300000 --seconds 3 --unpaced --coast
echo DONE
