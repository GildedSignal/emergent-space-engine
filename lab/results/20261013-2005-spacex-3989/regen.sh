#!/bin/sh
# Regenerates every number in dossier.md from the working tree + work/patch.diff.
# The patch is applied by the runner before this runs (it IS the working tree here).
# Cells: 5 bench runs x 2 arms, 8 s each, threads 1, paced 60 Hz — about 2 minutes total.
set -e
cd "$(dirname "$0")/../../.."
X=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-3}/release/xtask
cargo build --release -p xtask
run() { # tag, extra env, args...
  tag=$1; shift
  env "$@" $X universe --bench --seed "$SEED" --rtf "$RTF" --seconds 8 --members "$M" 2>/dev/null | \
    python3 -c "
import json,sys,re
r=json.load(sys.stdin); s=r['stats']
g=lambda k: re.search(k+r': (\d+)',s).group(1)
print('$tag'.ljust(22), 'digest', r['digest'][:12], 'bodies', r['bodies'], 'settle_ms', round(r['settle_ms']),
      'fleet_ms', round(r['engine_cost_by_kind'][4]['total_ms']), 'fleet_items', r['engine_cost_by_kind'][4]['items'],
      'ship_ms', round(r['engine_cost_by_kind'][2]['total_ms']), 'ship_items', r['engine_cost_by_kind'][2]['items'],
      'held', g('dormant_held'), 'woken', g('dormant_woken'), 'gate_checks', g('gate_checks'),
      'overflow', r['rtf']['overflow_frames'], '/480', 'p50cpu_ms', round(r['frame_cpu_ms']['p50'],2),
      'worstcpu_ms', round(r['frame_cpu_ms']['worst'],1), 'rtf_med', round(r['rtf']['median'],1))"
}
FAR=3221225472   # ES_PLAYER_ANGLE: the player opposite the fleet on the same circle (~14,000 km, co-orbital)

SEED=1 RTF=100 M=48    run "near48-s1-shipped"
SEED=1 RTF=100 M=48    run "near48-s1-dormant"   ES_DORMANT=1
SEED=1 RTF=100 M=1500  run "near1500-s1-shipped"
SEED=1 RTF=100 M=1500  run "near1500-s1-dormant" ES_DORMANT=1
SEED=1 RTF=100 M=1500  run "far1500-s1-shipped"  ES_PLAYER_ANGLE=$FAR
SEED=1 RTF=100 M=1500  run "far1500-s1-dormant"  ES_PLAYER_ANGLE=$FAR ES_DORMANT=1
SEED=3 RTF=100 M=1500  run "far1500-s3-shipped"  ES_PLAYER_ANGLE=$FAR
SEED=3 RTF=100 M=1500  run "far1500-s3-dormant"  ES_PLAYER_ANGLE=$FAR ES_DORMANT=1
SEED=1 RTF=1   M=4000  run "far4000-rtf1-shipped" ES_PLAYER_ANGLE=$FAR
SEED=1 RTF=1   M=4000  run "far4000-rtf1-dormant" ES_PLAYER_ANGLE=$FAR ES_DORMANT=1
