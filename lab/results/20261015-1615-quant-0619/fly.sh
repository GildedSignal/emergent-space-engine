#!/bin/bash
# Every flight in the dossier. One process at a time (10^5 scenes peak ~550 MB).
# Arms: ctl (shipped) / seam (ES_LAZY_ENTRY=1) / retain (ES_RETAIN=1, global)
#       hot (ES_RETAIN_HOT=<cap>, bounded FIFO) + cap probes + inertness control.
set -u
cd "$(dirname "$0")"
BIN=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-0}/release/examples/lazy_flight
mkdir -p flights
fly() { # name arm-envs... -- scene...
  local name=$1; shift
  local envs=(); while [ "$1" != "--" ]; do envs+=("$1"); shift; done; shift
  local f="flights/${name}_$(echo "$*" | tr ' ' '_').txt"
  echo "== $name $*"
  env "${envs[@]}" $BIN "$@" > "$f" 2>&1
  grep -h "^digest\|retained_now\|wall_s" "$f"
}
for scene in "10000 coast 20000 1" "100000 coast 20000 1" "10000 burn 20000 1" "100000 coast 48000 1"; do
  fly ctl    -u ES_LAZY_ENTRY -u ES_RETAIN -u ES_RETAIN_HOT       -- $scene
  fly seam   -u ES_RETAIN -u ES_RETAIN_HOT ES_LAZY_ENTRY=1        -- $scene
  fly retain -u ES_RETAIN_HOT ES_LAZY_ENTRY=1 ES_RETAIN=1         -- $scene
  fly hot    -u ES_RETAIN ES_LAZY_ENTRY=1 ES_RETAIN_HOT=4096      -- $scene
done
# Cap curve: where the hit share saturates (coast) and the working set (burn)
fly hot512   -u ES_RETAIN ES_LAZY_ENTRY=1 ES_RETAIN_HOT=512       -- 100000 coast 20000 1
fly hot65536 -u ES_RETAIN ES_LAZY_ENTRY=1 ES_RETAIN_HOT=65536     -- 100000 coast 20000 1
fly hot16384 -u ES_RETAIN ES_LAZY_ENTRY=1 ES_RETAIN_HOT=16384     -- 100000 coast 20000 1
fly hot16384 -u ES_RETAIN ES_LAZY_ENTRY=1 ES_RETAIN_HOT=16384     -- 100000 coast 48000 1
fly hot16384 -u ES_RETAIN ES_LAZY_ENTRY=1 ES_RETAIN_HOT=16384     -- 10000 burn 20000 1
fly hot65536 -u ES_RETAIN ES_LAZY_ENTRY=1 ES_RETAIN_HOT=65536     -- 10000 burn 20000 1
# Inertness: the bound without the seam is the shipped engine
fly hotnoseam -u ES_LAZY_ENTRY -u ES_RETAIN ES_RETAIN_HOT=4096    -- 10000 coast 20000 1
python3 table.py
