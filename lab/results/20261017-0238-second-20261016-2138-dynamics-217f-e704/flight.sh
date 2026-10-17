#!/bin/bash
# Interleaved A/B/C flight for the ratchet tax (lab run 20261017-0238-second-…-e704).
# usage: flight.sh <mode> <cells> <per> <stagger> <n1> <n2> <reps> <seed> [rate] [hz]
# Arms round-robin inside each rep so machine drift hits all arms equally.
set -u
REPO="$(cd "$(dirname "$0")/../../.." && pwd)"
BIN="${CARGO_TARGET_DIR:-$HOME/lab-target-0}/release/examples/tax"
mode=$1; cells=$2; per=$3; stagger=$4; n1=$5; n2=$6; reps=$7; seed=$8
rate=${9:-600}; hz=${10:-60}
echo "# flight mode=$mode cells=$cells per=$per stagger=$stagger n1=$n1 n2=$n2 reps=$reps seed=$seed rate=$rate hz=$hz"
echo "# load-before $(cut -d' ' -f1-3 /proc/loadavg)"
declare -a ARMS=("shipped|" "decay|ES_DECAY=1" "local|ES_LOCAL=1")
for rep in $(seq 1 "$reps"); do
  for spec in "${ARMS[@]}"; do
    name=${spec%%|*}; envs=${spec#*|}
    echo "# rep=$rep arm=$name $(date +%T) load=$(cut -d' ' -f1 /proc/loadavg)"
    if [ -z "$envs" ]; then
      "$BIN" "$mode" "$cells" "$per" "$stagger" "$n1" "$n2" "$seed" "$rate" "$hz" 2>&1 | grep '^RESULT'
    else
      env $envs "$BIN" "$mode" "$cells" "$per" "$stagger" "$n1" "$n2" "$seed" "$rate" "$hz" 2>&1 | grep '^RESULT'
    fi
  done
done
echo "# load-after $(cut -d' ' -f1-3 /proc/loadavg)"
