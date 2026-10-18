#!/usr/bin/env bash
# The flight arms: the flown plane (xtask universe --bench) with the census, the fix and the
# oracle. Each arm writes <arm>.json (stdout) and <arm>.cens (stderr: CENSUS/FIRE/PAIR).
# Usage: sweep.sh <out-dir> <xtask-binary>. Arms:
#   ship400off/on  shipped speed (2^15), 400 members: 37c1's no-ghost arm; on = bit-identity
#                  control (the fix must fire nothing and the digest must match off).
#   sd2off/on      speed_div 2, 48 members, seed 1: 37c1's 12.2% ghost arm.
#   sd2denseon     the dense (Chronon) stepper with the fix: must be cmp-identical to sd2on.
#   sd2m400off/on  speed_div 2, 400 members: 37c1's 46-ghost arm.
#   sd4on          speed_div 4, 48 members: the dose-response arm with the fix.
set -u
OUT=${1:?out dir}; BIN=${2:?xtask binary}
mkdir -p "$OUT"
run() { # arm seed members speed_div order fix
  local arm=$1 seed=$2 mem=$3 sd=$4 ord=$5 fix=$6
  echo "== arm $arm (seed $seed members $mem speed_div $sd order $ord fix $fix)" >&2
  SPACEX_CENSUS=1 SPACEX_ORACLE=1 SPACEX_FIX=$fix SPACEX_SPEED_DIV=$sd SPACEX_ORDER=$ord \
    timeout 120 "$BIN" universe --bench --unpaced --rtf 100 --seconds 30 --seed "$seed" --members "$mem" \
    >"$OUT/$arm.json" 2>"$OUT/$arm.cens" || echo "arm $arm FAILED" >&2
  echo "$arm: $(grep -c '^CENSUS' "$OUT/$arm.cens") census lines, $(grep -c '^FIRE' "$OUT/$arm.cens") fires"
}
run ship400off 1 400 32768 sparse 0
run ship400on  1 400 32768 sparse 1
run sd2off     1 48  2      sparse 0
run sd2on      1 48  2      sparse 1
run sd2denseon 1 48  2      dense  1
run sd2m400off 1 400 2      sparse 0
run sd2m400on  1 400 2      sparse 1
run sd4on      1 48  4      sparse 1
