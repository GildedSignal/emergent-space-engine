#!/bin/sh
# Regen (run 20261015-1450-library-3793): the runner applies work/patch.diff first.
# Reproduces every dossier number in ~6 min on the lab box (8 vCPU, <2 GB).
set -e
cd "$(git rev-parse --show-toplevel)"
R=lab/results/20261015-1450-library-3793
XT=/home/glmlab/lab-target-2/release/xtask

cargo build --release --locked --offline -p emergent-universe -p xtask

# 1) The three traced flights (seed 1, members 10^4, bench script, unpaced).
ES_KEYTRACE=1 ES_KEYTRACE_OUT=$R/work/trace10k.bin     $XT universe --bench --seed 1 --rtf 100   --seconds 55 --members 10000 --unpaced --no-record > $R/work/flight-5k.json
ES_KEYTRACE=1 ES_KEYTRACE_OUT=$R/work/trace10k-deep.bin $XT universe --bench --seed 1 --rtf 1000  --seconds 55 --members 10000 --unpaced --no-record > $R/work/flight-55k.json
ES_KEYTRACE=1 ES_KEYTRACE_OUT=$R/work/trace10k-1m.bin  $XT universe --bench --seed 1 --rtf 20000 --seconds 55 --members 10000 --unpaced --no-record > $R/work/flight-1m.json
grep -o '"keytrace.*' /dev/null || true

# 2) Digest identity: traced vs untraced (same seed/cut) must print one digest twice.
ES_KEYTRACE=1 ES_KEYTRACE_OUT=$R/work/dummy.bin $XT universe --bench --seed 1 --rtf 100 --seconds 10 --members 10000 --unpaced --no-record | grep '"digest"'
unset ES_KEYTRACE ES_KEYTRACE_OUT
$XT universe --bench --seed 1 --rtf 100 --seconds 10 --members 10000 --unpaced --no-record | grep '"digest"'
rm -f $R/work/dummy.bin

# 3) The replays: LRU / 2Q / MRU at K = 64..2048, full / post-burn-in / middle-third.
python3 $R/work/replay.py $R/work/trace10k.bin      $R/work/replay10k.json
python3 $R/work/replay.py $R/work/trace10k-deep.bin $R/work/replaydeep.json
python3 $R/work/replay.py $R/work/trace10k-1m.bin   $R/work/replay1m.json
python3 - <<'EOF'
import json
for f in ('replay10k.json','replaydeep.json','replay1m.json'):
    d=json.load(open('lab/results/20261015-1450-library-3793/work/'+f))
    r=d['post_burn_in']
    row=' '.join(f"K={K}:LRU{r['lru_%d'%K]:.3f}/2Q{r['2q_%d'%K]:.3f}" for K in (64,128,256,512))
    print(f, 'reads', d['reads'], 'distinct', d['distinct'], row)
EOF
