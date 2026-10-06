#!/bin/bash
# Loaded-vs-quiet pair: 6 CPU spinners (hogs) vs none, seeds 1 and 4, tail config.
cd "$(dirname "$0")/../../.." || exit 1
R=lab/results/20261006-1738-second-20261006-1436-quant-18e5-55ca/data
T=/home/glmlab/lab-target-3/release/xtask
rep () { python3 - "$1" "$2" <<'EOF'
import json,sys
d=json.load(open(sys.argv[1])); im=d['engine_item_max']; ph=im['player_item_phases_max_ms']
kinds={k['kind']:round(k['max_item_ms'],2) for k in d['engine_cost_by_kind']}
print(f"{sys.argv[2]:10s} worst_cpu={d['frame_cpu_ms']['worst']:6.1f} player_item={kinds['player']:6.2f} drain={ph['handout_drain']:6.2f} n={im['player_drain_members']:3d} enc={ph['encounters']:5.2f} h={d["hitch_counts"]}")
EOF
}
for mode in quiet loaded; do
  if [ "$mode" = loaded ]; then
    for i in 1 2 3 4 5 6; do (end=$((SECONDS+75)); while [ $SECONDS -lt $end ]; do :; done) & done
  fi
  sleep 1
  for s in 1 4; do
    PLANE_FRAME_DUMP="$R/L-$mode-$s.csv" $T universe --bench --seed $s --rtf 100 --members 480 --level 15 --seconds 30 > "$R/L-$mode-$s.json" 2>/dev/null
    rep "$R/L-$mode-$s.json" "$mode-s$s"
  done
  wait 2>/dev/null
done
