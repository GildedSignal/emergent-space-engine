#!/bin/bash
# The decisive arms: decision placement (canon|frame) x box load (quiet|loaded), N=1e5, cut 17000 gs.
# Usage: arms.sh <phase>  (quietA | quietD | loadB | loadC | loadEF | loadG2e5 | stopload)
set -u
R=/home/glmlab/actions-runner/_work/emergent-space-engine/lab-1
BIN=$CARGO_TARGET_DIR/release/examples/cut_digest
W=$R/lab/results/20261020-0229-inversion-4f1f/work
cd $W
one() { # tag, N, extra env...
  local tag=$1 n=$2; shift 2
  local la=$(cut -d' ' -f1-3 /proc/loadavg)
  env ES_FIX_PROBE=1 "$@" $BIN $n 17000 12 > runs/$tag.txt 2>&1
  echo "$tag load[$la] $(grep -o 'digest [0-9a-f]\{8\}' runs/$tag.txt | head -1) $(grep -o 'kicks [0-9]*' runs/$tag.txt | head -1) $(grep -o 'encounters [0-9]*' runs/$tag.txt | head -1) $(grep -o 'stale [0-9]*' runs/$tag.txt | head -1) $(grep -o 'stale_enc [0-9]*' runs/$tag.txt | head -1)"
}
startload() { for i in 1 2 3 4 5 6; do setsid bash -c 'while :; do :; done' >/dev/null 2>&1 & echo $! >> /tmp/spin4f1f.pids; done; sleep 2; echo "load: $(cut -d' ' -f1-3 /proc/loadavg)"; }
stopload() { [ -f /tmp/spin4f1f.pids ] && kill $(cat /tmp/spin4f1f.pids) 2>/dev/null; rm -f /tmp/spin4f1f.pids; sleep 1; echo "load after stop: $(cut -d' ' -f1-3 /proc/loadavg)"; }
mkdir -p runs
case ${1:-} in
  quietA) for i in 1 2 3 4; do one canon_on_quiet_$i 100000 ES_ROOT_SHIPS_TO_QUEUE=1; done;;
  quietD) for i in 1 2 3 4; do one frame_on_quiet_$i 100000 ES_ROOT_SHIPS_TO_QUEUE=1 ES_DECIDE=frame; done
          one frame_off_quiet_1 100000 ES_DECIDE=frame;;
  loadup) startload;;
  loaddown) stopload;;
  loadB) for i in 1 2 3 4 5 6 7 8; do one canon_on_load_$i 100000 ES_ROOT_SHIPS_TO_QUEUE=1; done;;
  loadC) for i in 1 2 3; do one canon_off_load_$i 100000; done;;
  loadEF) for i in 1 2 3 4 5 6; do one frame_on_load_$i 100000 ES_ROOT_SHIPS_TO_QUEUE=1 ES_DECIDE=frame; done
          for i in 1 2; do one frame_off_load_$i 100000 ES_DECIDE=frame; done;;
  loadG2e5) for i in 1 2 3; do one canon_on_2e5_load_$i 200000 ES_ROOT_SHIPS_TO_QUEUE=1; done
            one canon_off_2e5_load_1 200000;;
  *) echo "phases: quietA quietD loadup loaddown loadB loadC loadEF loadG2e5";;
esac
