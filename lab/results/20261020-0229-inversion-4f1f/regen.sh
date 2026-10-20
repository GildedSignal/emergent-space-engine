#!/bin/bash
# Regen for 20261020-0229-inversion-4f1f. The runner applies work/patch.diff (4063's instrument
# patch verbatim + this run's ES_DECIDE=frame addition) before this runs. ~11 min on a quiet box.
# NOTE the law being regenerated: canon-anchored arms are DIGEST-STABLE (exact digits reproduce);
# frame-anchored arms under load are MULTISTABLE — the exact digest multiset is schedule-born,
# which is the finding. The run's own flights are frozen in work/runs/ and work/runs.txt.
set -u
R=/home/glmlab/actions-runner/_work/emergent-space-engine/lab-1
W=$R/lab/results/20261020-0229-inversion-4f1f/work
cd $W
BIN=$CARGO_TARGET_DIR/release/examples/cut_digest
cargo build --release -p emergent-universe --example cut_digest 2>&1 | tail -1
one() { local tag=$1 n=$2; shift 2; local la=$(cut -d' ' -f1-3 /proc/loadavg)
  env ES_FIX_PROBE=1 "$@" $BIN $n 17000 12 > regen_runs/$tag.txt 2> regen_runs/$tag.err
  local tick=$(grep -h . regen_runs/$tag.err | grep -o 'tick [0-9-]*' | head -1)
  echo "$tag load[$la] $(grep -o 'digest [0-9a-f]\{8\}' regen_runs/$tag.txt|head -1) $(grep -o 'kicks [0-9]*' regen_runs/$tag.txt) $(grep -o 'encounters [0-9]*' regen_runs/$tag.txt) stale$(grep -o 'stale [0-9]*' regen_runs/$tag.txt|grep -o '[0-9]*') $tick"; }
stopload() { [ -f /tmp/spin4f1f.pids ] && kill $(cat /tmp/spin4f1f.pids) 2>/dev/null; rm -f /tmp/spin4f1f.pids; sleep 1; }
trap stopload EXIT
rm -rf regen_runs; mkdir -p regen_runs
echo "== quiet (expect: canon arms 581ced1a stable; frame arms 0b9930b6 stable, decision tick 199980)"
one q_off_canon 100000
one q_on_canon 100000 ES_ROOT_SHIPS_TO_QUEUE=1
one q_on_canon2 100000 ES_ROOT_SHIPS_TO_QUEUE=1
one q_off_frame 100000 ES_DECIDE=frame
one q_off_frame2 100000 ES_DECIDE=frame
one q_on_frame 100000 ES_ROOT_SHIPS_TO_QUEUE=1 ES_DECIDE=frame
echo "== loaded (6 spinners; expect: canon arms STILL 581ced1a; frame arms >=2 distinct digests, ticks < 199980 varying)"
for i in 1 2 3 4 5 6; do setsid bash -c 'while :; do :; done' >/dev/null 2>&1 & echo $! >> /tmp/spin4f1f.pids; done; sleep 2
one l_on_canon 100000 ES_ROOT_SHIPS_TO_QUEUE=1
one l_on_canon2 100000 ES_ROOT_SHIPS_TO_QUEUE=1
one l_on_canon3 100000 ES_ROOT_SHIPS_TO_QUEUE=1
one l_off_canon 100000
one l_off_canon2 100000
for i in 1 2 3 4; do one l_off_frame_$i 100000 ES_DECIDE=frame; done
for i in 1 2 3 4; do one l_on_frame_$i 100000 ES_ROOT_SHIPS_TO_QUEUE=1 ES_DECIDE=frame; done
echo "== optional 2e5 spot (skip with REGEN_SKIP_2E5=1)"
if [ -z "${REGEN_SKIP_2E5:-}" ]; then
  for i in 1 2; do one l_off_frame_2e5_$i 200000 ES_DECIDE=frame; done
fi
stopload
echo "== summary: distinct digests per cell"
for cell in q_off_canon q_on_canon q_off_frame q_on_frame l_on_canon l_off_canon l_off_frame l_on_frame; do
  echo "$cell: $(grep -h -o 'digest [0-9a-f]\{8\}' regen_runs/${cell}*.txt | sort | uniq -c | tr '\n' ' ')"
done
