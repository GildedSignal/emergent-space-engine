#!/bin/bash
# Bursty load (a shared box's real pattern: other runs start/stop), vs the steady spinners.
# 4 spinners, each on/off with random duty, for the duration of the arms given as args.
set -u
R=/home/glmlab/actions-runner/_work/emergent-space-engine/lab-1
W=$R/lab/results/20261020-0229-inversion-4f1f/work
cd $W
stopburst() { [ -f /tmp/burst4f1f.pids ] && kill $(cat /tmp/burst4f1f.pids) 2>/dev/null; rm -f /tmp/burst4f1f.pids; sleep 1; echo "burst stopped: $(cut -d' ' -f1-3 /proc/loadavg)"; }
trap stopburst EXIT
for i in 1 2 3 4; do
  setsid bash -c 'while :; do h=$((RANDOM % 300 + 50)); l=$((RANDOM % 200 + 20)); end=$((SECONDS + h/100)); while [ $SECONDS -lt $end ]; do :; done; sleep 0.0$l; done' >/dev/null 2>&1 &
  echo $! >> /tmp/burst4f1f.pids
done
sleep 2
BIN=$CARGO_TARGET_DIR/release/examples/cut_digest
one() { local tag=$1 n=$2; shift 2; local la=$(cut -d' ' -f1-3 /proc/loadavg)
  env ES_FIX_PROBE=1 "$@" $BIN $n 17000 12 > runs/$tag.txt 2>&1
  echo "$tag load[$la] $(grep -o 'digest [0-9a-f]\{8\}' runs/$tag.txt | head -1) $(grep -o 'kicks [0-9]*' runs/$tag.txt | head -1) $(grep -o 'encounters [0-9]*' runs/$tag.txt | head -1) $(grep -o 'stale [0-9]*' runs/$tag.txt | head -1) $(grep -o 'stale_enc [0-9]*' runs/$tag.txt | head -1)"; }
for i in 1 2 3 4 5 6; do one canon_on_burst_$i 100000 ES_ROOT_SHIPS_TO_QUEUE=1; done
for i in 1 2; do one frame_on_burst_$i 100000 ES_ROOT_SHIPS_TO_QUEUE=1 ES_DECIDE=frame; done
