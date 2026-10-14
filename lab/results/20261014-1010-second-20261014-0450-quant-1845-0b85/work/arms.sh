#!/usr/bin/env bash
# The decisive A/B: one prof binary, ES_IMP_WARM off/on, five arms. ~4 min on 8 vCPU.
set -euo pipefail
W="$(cd "$(dirname "$0")" && pwd)"
XT=${XT:-/tmp/rl-0b85/release/xtask-prof}
export ES_MEMBERS=1000000
arm() { # name seed rtf members
  local name=$1 seed=$2 rtf=$3 m=$4
  if [ ! -s "$W/$name-off.json" ]; then
    $XT universe --bench --seed "$seed" --rtf "$rtf" --seconds 8 --members "$m" > "$W/$name-off.json" 2> "$W/$name-off.err"
  fi
  if [ ! -s "$W/$name-on.json" ]; then
    ES_IMP_WARM=1 $XT universe --bench --seed "$seed" --rtf "$rtf" --seconds 8 --members "$m" > "$W/$name-on.json" 2> "$W/$name-on.err"
  fi
}
arm m4000-s3   3 1   4000
arm m1500-s3   3 1   1500
arm m4000-s7   7 1   4000
arm m400-s3-f  3 100 400
arm m16000-s3  3 1   16000
echo done
