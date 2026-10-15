#!/bin/bash
# The knee matrix: burn working set WS(N) vs cap. One process at a time.
set -u
cd "$(dirname "$0")"
BIN=$PWD/bin/lazy_flight-0619
mkdir -p flights
fly() { local name=$1; shift; local envs=(); while [ "$1" != "--" ]; do envs+=("$1"); shift; done; shift
  local f="flights/${name}_$(echo "$*" | tr ' ' '_').txt"
  echo "== $name $*"
  env "${envs[@]}" $BIN "$@" > "$f" 2>&1
  grep -h "^digest\|demotions\|retain hits\|wall_s" "$f" | head -4
}
HOT() { echo "-u ES_RETAIN ES_LAZY_ENTRY=1 ES_RETAIN_HOT=$1"; }
# N = 1e5 first (ties to 0757's checker's cap-262144 point)
for a in "ctl|-u ES_LAZY_ENTRY -u ES_RETAIN -u ES_RETAIN_HOT" "glob|-u ES_RETAIN_HOT ES_LAZY_ENTRY=1 ES_RETAIN=1" \
         "sat|$(HOT 1048576)" "c262144|$(HOT 262144)" "c65536|$(HOT 65536)" "c16384|$(HOT 16384)"; do
  n=${a%%|*}; fly $n ${a#*|} -- 100000 burn 20000 1
done
# N = 3e4
for a in "ctl|-u ES_LAZY_ENTRY -u ES_RETAIN -u ES_RETAIN_HOT" "glob|-u ES_RETAIN_HOT ES_LAZY_ENTRY=1 ES_RETAIN=1" \
         "sat|$(HOT 1048576)" "c65536|$(HOT 65536)" "c16384|$(HOT 16384)"; do
  n=${a%%|*}; fly $n ${a#*|} -- 30000 burn 20000 1
done
# N = 2e5
for a in "ctl|-u ES_LAZY_ENTRY -u ES_RETAIN -u ES_RETAIN_HOT" "glob|-u ES_RETAIN_HOT ES_LAZY_ENTRY=1 ES_RETAIN=1" \
         "sat|$(HOT 1048576)" "c131072|$(HOT 131072)" "c65536|$(HOT 65536)" "c16384|$(HOT 16384)"; do
  n=${a%%|*}; fly $n ${a#*|} -- 200000 burn 20000 1
done
# held-out seed 7 at 1e5 + cut dependence
fly s7sat   $(HOT 1048576) -- 100000 burn 20000 7
fly s7c65536 $(HOT 65536)  -- 100000 burn 20000 7
fly cut48sat $(HOT 1048576) -- 100000 burn 48000 1
# the 1e4 knee point (cited as WS=40,187) and the seed-7 shipped control
fly sat $(HOT 65536) -- 10000 burn 20000 1
fly ctl -u ES_LAZY_ENTRY -u ES_RETAIN -u ES_RETAIN_HOT -- 100000 burn 20000 7
