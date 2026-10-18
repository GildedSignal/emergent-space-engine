#!/usr/bin/env bash
# The decisive sweep. Each arm: fly the plane headless, census contacts at the resolver gate.
# Usage: sweep.sh <out-dir> [binary]. Writes <out-dir>/<arm>.cens and <arm>.json per arm.
set -u
OUT=${1:?out dir}; BIN=${2:-/home/glmlab/lab-target-1/release/xtask}
mkdir -p "$OUT"
run() { # arm seed members speed_div order
  local arm=$1 seed=$2 mem=$3 sd=$4 ord=$5
  echo "== arm $arm (seed $seed members $mem speed_div $sd order $ord)" >&2
  SPACEX_CENSUS=1 SPACEX_SPEED_DIV=$sd SPACEX_ORDER=$ord timeout 120 "$BIN" universe \
    --bench --unpaced --rtf 100 --seconds 30 --seed "$seed" --members "$mem" \
    >"$OUT/$arm.json" 2>"$OUT/$arm.cens" || echo "arm $arm FAILED" >&2
  grep -c CENSUS "$OUT/$arm.cens" || true
}
run ship48    1 48  32768 sparse
run ship400   1 400 32768 sparse
run sd128     1 48  128   sparse
run sd8       1 48  8     sparse
run sd2       1 48  2     sparse
run sd2dense  1 48  2     dense
run sd2s2     2 48  2     sparse
run sd2d2     2 48  2     dense
run sd4       1 48  4     sparse
run sd2m400   1 400 2     sparse
