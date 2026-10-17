#!/bin/bash
# D4: the checker's confounded 28,160-body datum, paired, digests captured.
set -u
R="$(cd "$(dirname "$0")" && pwd)/work"; BIN=/home/glmlab/lab-target-0/release/examples/tax
run() { local name=$1 tmo=$2 envs=$3; shift 3
  echo "== $name load $(cut -d' ' -f1-3 /proc/loadavg) $(date +%T) ==" >>"$R/battery.log"
  if [ -n "$envs" ]; then timeout "$tmo" env $envs "$BIN" "$@" >"$R/$name.log" 2>&1
  else timeout "$tmo" "$BIN" "$@" >"$R/$name.log" 2>&1; fi
  echo "$name rc=$? panics=$(grep -c panicked "$R/$name.log") $(date +%T)" >>"$R/battery.log"; }
run D4-cap64   400 "ES_CAP=64" batch 2560 8 30 1 1500 1
run D4-shipped 400 ""          batch 2560 8 30 1 1500 1
echo D4-DONE $(date +%T) >>"$R/battery.log"
