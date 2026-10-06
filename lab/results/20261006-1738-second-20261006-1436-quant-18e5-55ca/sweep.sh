#!/bin/bash
# Decisive sweep for the second-author run. Each bench ≤ 31 s wall.
cd "$(dirname "$0")/../../.." || exit 1
R=lab/results/20261006-1738-second-20261006-1436-quant-18e5-55ca/data
T=/home/glmlab/lab-target-3/release/xtask
run () { # name, extra args...
  local name=$1; shift
  echo "=== $name $(date +%H:%M:%S) load:$(cut -d' ' -f1-3 /proc/loadavg)" >> "$R/sweep.log"
  PLANE_FRAME_DUMP="$R/$name.csv" $T universe --bench --seed "${SEED:-1}" --rtf "${RTF:-100}" \
    --members "${MEM:-480}" --level "${LVL:-15}" --seconds "${SECS:-30}" "$@" \
    > "$R/$name.json" 2> "$R/$name.err"
  python3 - "$R/$name.json" "$name" <<'EOF'
import json,sys
d=json.load(open(sys.argv[1]))
im=d['engine_item_max']; ph=im['player_item_phases_max_ms']
kinds={k['kind']:(round(k['max_item_ms'],2),k['items']) for k in d['engine_cost_by_kind']}
print(f"{sys.argv[2]:8s} seed{d['seed']} worst_cpu={d['frame_cpu_ms']['worst']:6.1f} eng_max={d['where_the_time_goes_ms']['engine']['max']:6.1f} h={d['hitch_counts']} player_item={kinds['player'][0]:6.2f}ms drain={ph['handout_drain']:6.2f}ms n={im['player_drain_members']:3d} enc={ph['encounters']:5.2f} fleets={ph['fleets_catchup']:5.2f} pull={ph['ship_lane_pull']:5.2f} step={ph['step_apply']:5.2f} fleet_item={kinds['fleet'][0]:5.2f} ship_item={kinds['ship'][0]:5.2f} handout={im['handout_max_ms']:5.2f} dig={d['digest'][:8]}@{d['cut_tick']}")
EOF
}
export -f run 2>/dev/null || true
mkdir -p "$R"
: > "$R/sweep.log"
# 1) quiet seed sweep at the tail config
for s in 1 2 3 4 5 6; do SEED=$s run "q$s"; done
# 2) budget dial on seed 1
run e2b --engine-ms 20
# 3) m48/l0 paced + unpaced (the a/g pair) for the paced factor
MEM=48 LVL=0 run a
MEM=48 LVL=0 run g --unpaced
# 4) 4800/l0 seed 1 (the c config, for the view-share number)
MEM=4800 LVL=0 run c1
