#!/bin/sh
# P2: run-to-run digest stability under concurrent load — the checker's probe, twice.
# Four identical dormant runs at seed 3, far scene, in parallel; one digest expected per batch.
set -e
cd "$(dirname "$0")/../../../.."
X=${1:-${CARGO_TARGET_DIR:-/home/glmlab/lab-target-3}/release/xtask}
FAR=3221225472
for batch in 1 2; do
  echo "--- load batch $batch (4 concurrent dormant, seed 3) ---"
  for i in 1 2 3 4; do
    env ES_DORMANT=1 ES_PLAYER_ANGLE=$FAR $X universe --bench --seed 3 --rtf 100 --seconds 8 --members 1500 2>/dev/null | \
      python3 -c "
import json,sys,re; r=json.load(sys.stdin); s=r['stats']
g=lambda k: re.search(k+r': (\d+)',s).group(1)
print('batch$batch', r['digest'][:12], 'held', g('dormant_held'), 'woken', g('dormant_woken'), 'cut', r['cut_tick'])" &
  done
  wait
done
echo '--- shipped control under the same load ---'
for i in 1 2 3 4; do
  env ES_PLAYER_ANGLE=$FAR $X universe --bench --seed 3 --rtf 100 --seconds 8 --members 1500 2>/dev/null | \
    python3 -c "import json,sys; r=json.load(sys.stdin); print('ctl', r['digest'][:12])" &
done
wait
