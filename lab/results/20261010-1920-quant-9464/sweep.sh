#!/bin/bash
# The plane's capacity ladder: members scaling, unpaced (work per presented frame), rtf 1.
# Each run's JSON lands beside this script. Wall cap per run: ~55 s.
set -u
cd /home/glmlab/actions-runner/_work/emergent-space-engine/lab-2
X=/home/glmlab/lab-target-2/release/xtask
OUT=$(dirname "$0")
run () { # name args...
  local name=$1; shift
  local t0=$(date +%s)
  "$X" universe --bench "$@" > "$OUT/$name.json" 2> "$OUT/$name.err"
  local rc=$?
  echo "$name rc=$rc wall=$(( $(date +%s) - t0 ))s"
}
# in-frame ladder (extent wall predicted near 1300)
run n48      --members 48    --rtf 1 --seconds 10 --unpaced
run n192     --members 192   --rtf 1 --seconds 10 --unpaced
run n512     --members 512   --rtf 1 --seconds 10 --unpaced
run n1024    --members 1024  --rtf 1 --seconds 10 --unpaced
run n1536    --members 1536  --rtf 1 --seconds 10 --unpaced
# past the wall: mixed frame+tubes regime
run n2048    --members 2048  --rtf 1 --seconds 5  --unpaced
run n8192    --members 8192  --rtf 1 --seconds 3  --unpaced
run n32768   --members 32768 --rtf 1 --seconds 1  --unpaced
run n131072  --members 131072 --rtf 1 --seconds 1 --unpaced
# determinism controls
run n512again --members 512  --rtf 1 --seconds 10 --unpaced
run n512paced --members 512  --rtf 1 --seconds 10
# threads rung (kick pass parallelism; same digest required)
run n65536t1 --members 65536 --rtf 1 --seconds 1 --unpaced --threads 1
run n65536t4 --members 65536 --rtf 1 --seconds 1 --unpaced --threads 4
# rtf rung: game-time advance per frame x100
run n1024rtf100 --members 1024 --rtf 100 --seconds 2 --unpaced
