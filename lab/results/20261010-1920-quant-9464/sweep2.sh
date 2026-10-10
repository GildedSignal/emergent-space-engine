#!/bin/bash
# The real capacity ladder (clamp lifted): in-frame rungs to the extent wall, past it, then rtf 100.
set -u
cd /home/glmlab/actions-runner/_work/emergent-space-engine/lab-2
X=/home/glmlab/lab-target-2/release/xtask
OUT=$(dirname "$0")
run () {
  local name=$1; shift
  local t0=$(date +%s)
  timeout 70 "$X" universe --bench "$@" > "$OUT/$name.json" 2> "$OUT/$name.err"
  local rc=$?
  echo "$name rc=$rc wall=$(( $(date +%s) - t0 ))s"
}
# rtf 1: the presentation floor (readout scaling), battle dormant
run m48       --members 48     --rtf 1 --seconds 10 --unpaced
run m400      --members 400    --rtf 1 --seconds 10 --unpaced
run m1024     --members 1024   --rtf 1 --seconds 10 --unpaced
run m1300     --members 1300   --rtf 1 --seconds 10 --unpaced
run m2048     --members 2048   --rtf 1 --seconds 5  --unpaced
run m8192     --members 8192   --rtf 1 --seconds 3  --unpaced
run m32768    --members 32768  --rtf 1 --seconds 1  --unpaced
# rtf 100: the flight regime (epochs and contacts fire)
run r100m400  --members 400    --rtf 100 --seconds 2 --unpaced
run r100m1024 --members 1024   --rtf 100 --seconds 2 --unpaced
run r100m1300 --members 1300   --rtf 100 --seconds 2 --unpaced
run r100m2048 --members 2048   --rtf 100 --seconds 1 --unpaced
# determinism controls at honest sizes
run m1024dup  --members 1024   --rtf 1 --seconds 10 --unpaced
run m1024t4   --members 1300   --rtf 100 --seconds 2 --unpaced --threads 4
