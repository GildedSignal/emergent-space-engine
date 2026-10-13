#!/bin/sh
# Regenerates every number in dossier.md from the working tree + work/patch.diff (applied by the
# runner before this runs). Private target dir: the lab's shared default (lab-target-3) is a race
# between windows — a concurrent window's build replaced the binary mid-run in this run's first
# matrix attempt (its cells then printed stats without the probe's fields).
# About 12 minutes: 1 build + ~30 bench cells (8 s each, threads 1, paced 60 Hz).
set -e
cd "$(dirname "$0")/../../.."
T=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-bc2b}
X=$T/release/xtask
cargo build --release -p xtask
FAR=3221225472   # ES_PLAYER_ANGLE: the player opposite the fleet on the same circle (~14,000 km, co-orbital)

run() { # tag, seed, rtf, members, seconds, then env assignments
  tag=$1; seed=$2; rtf=$3; m=$4; secs=$5; shift 5
  env "$@" $X universe --bench --seed "$seed" --rtf "$rtf" --seconds "$secs" --members "$m" 2>/dev/null | \
    python3 -c "
import json,sys,re
r=json.load(sys.stdin); s=r['stats']
g=lambda k: re.search(k+r': (\d+)',s).group(1)
print('$tag'.ljust(24), 'digest', r['digest'][:12], 'bodies', r['bodies'], 'held', g('dormant_held'),
      'woken', g('dormant_woken'), 'checks', g('gate_checks'), 'enc', g('encounters'),
      'ovf', r['rtf']['overflow_frames'], '/480', 'p50ms', round(r['frame_cpu_ms']['p50'],2),
      'worst', round(r['frame_cpu_ms']['worst'],1), 'rtf_med', round(r['rtf']['median'],1),
      'settle_ms', round(r['settle_ms']), 'cut', r['cut_tick'])"
}

echo '--- budget sweep (fixed): one digest at every engine-ms, work moves flight<->settle only ---'
for MS in 0.5 5 100; do
  env ES_DORMANT=1 ES_PLAYER_ANGLE=$FAR $X universe --bench --seed 3 --rtf 100 --seconds 8 --members 1500 --engine-ms $MS 2>/dev/null | \
    python3 -c "
import json,sys,re; r=json.load(sys.stdin)
f=r['fleet']; g=lambda k: re.search(k+r': (\d+)',r['stats']).group(1)
print(('fixed-ms%s'%'$MS').ljust(24), r['digest'][:12], 'fleet tick', f['tick'], 'handoffs', f['handoffs'], 'members', f['members'],
      'held', g('dormant_held'), 'ovf', r['rtf']['overflow_frames'], 'bodies', r['bodies'])"
done

echo '--- P1: identity across seeds, far scene, 1500/rtf100 (drift rule) ---'
for SEED in 1 3 7 11; do
  run "far1500-s$SEED-shipped" $SEED 100 1500 8 ES_PLAYER_ANGLE=$FAR
  run "far1500-s$SEED-dormant" $SEED 100 1500 8 ES_PLAYER_ANGLE=$FAR ES_DORMANT=1
done

echo '--- P1b: identity with the canon-exact doll rule ---'
run "far1500-s3-doll"  3 100 1500 8 ES_PLAYER_ANGLE=$FAR ES_DORMANT=1 ES_DORMANT_WAKE=doll
run "far1500-s7-doll"  7 100 1500 8 ES_PLAYER_ANGLE=$FAR ES_DORMANT=1 ES_DORMANT_WAKE=doll

echo '--- P5: near scene (positive control) ---'
run "near48-s1-shipped"   1 100 48   8 ES_X=1
run "near48-s1-dormant"   1 100 48   8 ES_DORMANT=1
run "near1500-s1-shipped" 1 100 1500 8 ES_X=1
run "near1500-s1-dormant" 1 100 1500 8 ES_DORMANT=1

echo '--- P6: 4000/rtf1 (the collapse rung), both rules ---'
run "far4000-rtf1-shipped" 1 1 4000 8 ES_PLAYER_ANGLE=$FAR
run "far4000-rtf1-dormant" 1 1 4000 8 ES_PLAYER_ANGLE=$FAR ES_DORMANT=1
run "far4000-rtf1-doll"    1 1 4000 8 ES_PLAYER_ANGLE=$FAR ES_DORMANT=1 ES_DORMANT_WAKE=doll

echo '--- P3: the canon-exact rule price, far 1500/rtf100 seed 3 ---'
run "far1500-s3-doll-cost" 3 100 1500 8 ES_PLAYER_ANGLE=$FAR ES_DORMANT=1 ES_DORMANT_WAKE=doll

echo '--- the next decade: 8000/rtf100, 4 s ---'
run "far8000-shipped" 1 100 8000 4 ES_PLAYER_ANGLE=$FAR
run "far8000-dormant" 1 100 8000 4 ES_PLAYER_ANGLE=$FAR ES_DORMANT=1

echo '--- P2: load stability (the checker probe, twice) + shipped control ---'
for batch in 1 2; do
  for i in 1 2 3 4; do
    env ES_DORMANT=1 ES_PLAYER_ANGLE=$FAR $X universe --bench --seed 3 --rtf 100 --seconds 8 --members 1500 2>/dev/null | \
      python3 -c "import json,sys; r=json.load(sys.stdin); print('load-batch$batch', r['digest'][:12])" &
  done; wait
done
for i in 1 2 3 4; do
  env ES_PLAYER_ANGLE=$FAR $X universe --bench --seed 3 --rtf 100 --seconds 8 --members 1500 2>/dev/null | \
    python3 -c "import json,sys; r=json.load(sys.stdin); print('load-ctl', r['digest'][:12])" &
done; wait
