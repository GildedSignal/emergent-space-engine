#!/bin/sh
# The decisive matrix of the second-author run: identity across seeds/rules, budget and load
# stability, and the canon-exact rule's price. Each cell: `universe --bench`, 8 s, threads 1,
# paced 60 Hz. Usage: sh matrix.sh [release-binary]
set -e
cd "$(dirname "$0")/../../../.."
X=${1:-${CARGO_TARGET_DIR:-/home/glmlab/lab-target-3}/release/xtask}
FAR=3221225472   # ES_PLAYER_ANGLE: the player opposite the fleet on the same circle (~14,000 km, co-orbital)

run() { # tag, extra env, args...
  tag=$1; shift
  env "$@" $X universe --bench --seed "$SEED" --rtf "$RTF" --seconds "$SECS" --members "$M" 2>/dev/null | \
    python3 -c "
import json,sys,re
r=json.load(sys.stdin); s=r['stats']
g=lambda k: re.search(k+r': (\d+)',s).group(1)
print('$tag'.ljust(26), 'digest', r['digest'][:12], 'bodies', r['bodies'], 'held', g('dormant_held'),
      'woken', g('dormant_woken'), 'checks', g('gate_checks'),
      'enc', g('encounters'), 'ovf', r['rtf']['overflow_frames'], '/480',
      'p50ms', round(r['frame_cpu_ms']['p50'],2), 'worst', round(r['frame_cpu_ms']['worst'],1),
      'rtf_med', round(r['rtf']['median'],1), 'settle_ms', round(r['settle_ms']))"
}

echo '--- P1: identity across seeds, far scene, 1500/rtf100 (drift rule) ---'
for SEED in 1 3 7 11; do RTF=100 M=1500 SECS=8
  run "far1500-s$SEED-shipped"  ES_PLAYER_ANGLE=$FAR
  run "far1500-s$SEED-dormant"  ES_PLAYER_ANGLE=$FAR ES_DORMANT=1
done

echo '--- P1b: identity with the canon-exact doll rule (seeds 3, 7) ---'
for SEED in 3 7; do RTF=100 M=1500 SECS=8
  run "far1500-s$SEED-doll"     ES_PLAYER_ANGLE=$FAR ES_DORMANT=1 ES_DORMANT_WAKE=doll
done

echo '--- P5: near scene (positive control), seed 1 ---'
RTF=100 SEED=1 SECS=8
M=48    run "near48-s1-shipped"
M=48    run "near48-s1-dormant" ES_DORMANT=1
M=1500  run "near1500-s1-shipped"
M=1500  run "near1500-s1-dormant" ES_DORMANT=1

echo '--- P6: fermi collapse rung 4000/rtf1, both rules ---'
RTF=1 SEED=1 M=4000 SECS=8
run "far4000-rtf1-shipped"  ES_PLAYER_ANGLE=$FAR
run "far4000-rtf1-dormant"  ES_PLAYER_ANGLE=$FAR ES_DORMANT=1
run "far4000-rtf1-doll"     ES_PLAYER_ANGLE=$FAR ES_DORMANT=1 ES_DORMANT_WAKE=doll

echo '--- P3: the canon-exact rule price, far 1500/rtf100 seed 3 (already have shipped+dormant above) ---'
RTF=100 SEED=3 M=1500 SECS=8
run "far1500-s3-doll-cost"  ES_PLAYER_ANGLE=$FAR ES_DORMANT=1 ES_DORMANT_WAKE=doll
