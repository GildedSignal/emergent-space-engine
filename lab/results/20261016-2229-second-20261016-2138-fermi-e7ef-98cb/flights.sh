#!/bin/bash
# The decisive flight matrix (predictions.md already written). Sequential on purpose: wall
# timings on a shared box. Each arm appends its full output to flights/.
set -u
cd "$(dirname "$0")"
mkdir -p flights
NL=${NL:-$(cd ../../.. && cargo metadata --format-version 1 --no-deps | python3 -c "import json,sys; print(json.load(sys.stdin)['target_directory'])")/release/examples/nladder}
run() { # run <tag> <envs...> -- <nladder args...>
  local tag=$1; shift
  local envs=()
  while [ "$1" != "--" ]; do envs+=("$1"); shift; done
  shift
  echo "== $tag: env=${envs[*]} args=$*"
  env "${envs[@]}" LADDER_GUARD_S=${GUARD:-55} timeout 150 "$NL" "$@" >"flights/$tag.txt" 2>&1
  grep -E "rung|frames after|game |freeze:|impact_guess" "flights/$tag.txt"
}
export GUARD=80
run S3-ship-3e5-1800  -- 300000 coast 32 1800
run C5-comp-3e5-1800  BELT_SPLIT=1 STAGGER_GENESIS=1 -- 300000 coast 75 1800
run C6-comp-3e5-3600  BELT_SPLIT=1 STAGGER_GENESIS=1 -- 300000 coast 40 3600
run C7-comp-3e5-7200  BELT_SPLIT=1 STAGGER_GENESIS=1 -- 300000 coast 22 7200
run S1-ship-1e5-1800  -- 100000 coast 35 1800
run C1-comp-1e5-1800  BELT_SPLIT=1 STAGGER_GENESIS=1 -- 100000 coast 75 1800
run C4-comp-1e5-14400 BELT_SPLIT=1 STAGGER_GENESIS=1 -- 100000 coast 14 14400
export GUARD=55
run AB0-guess-off-1e5-3600 BELT_SPLIT=1 STAGGER_GENESIS=1 IMPACT_GUESS=0 -- 100000 coast 25 3600
run AB1-guess-on-1e5-3600  BELT_SPLIT=1 STAGGER_GENESIS=1 IMPACT_GUESS=1 -- 100000 coast 25 3600
echo DONE
