#!/bin/sh
# Regen: every number in dossier.md, from shipped code + work/patch.diff (applied before this runs).
# ≤ 6 min on 8 vCPU. Linux/x86 shared box: orders of magnitude only.
set -e
cd "$(dirname "$0")/../../.."   # repo root (lab/results/<run>/ -> root)
R=lab/results/20261016-0504-system-e070
mkdir -p $R/out

# 0. Off-arm identity: this patch (already applied by the runner) vs pristine main.
cargo build --release -p xtask 2>&1 | tail -1
B=$(cargo metadata --no-deps --format-version 1 | python3 -c "import json,sys; print(json.load(sys.stdin)['target_directory'])")/release/xtask
$B universe --bench --rtf 100 --seconds 20 --seed 1 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['digest'])" > $R/out/patched_off_digest.txt
git stash -q
cargo build --release -p xtask 2>&1 | tail -1
$B universe --bench --rtf 100 --seconds 20 --seed 1 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['digest'])" > $R/out/pristine_digest.txt
git stash pop -q
cargo build --release -p xtask 2>&1 | tail -1
diff $R/out/pristine_digest.txt $R/out/patched_off_digest.txt && echo OFF_ARM_IDENTICAL

# 1. The flight matrix (budget-free, engine-only, traced): worst-bucket anatomy + frame_events + kicks.
fly(){ name=$1; seed=$2; extra=$3; shift 3
  env ES_ENGINE_ONLY=1 ES_TRACE=1 "$@" $B universe --bench --unpaced --engine-ms 100000 \
      --rtf 1000 --seconds 30 --seed $seed --extra $extra > $R/out/$name.json 2>/dev/null
}
fly storm_s1     1 10000
fly nolocals_s1  1 10000 ES_NO_LOCALS=1
fly stagger_s1   1 10000 ES_STAGGER_LOCALS=24
fly storm_s7     7 10000
fly stagger_s7   7 10000 ES_STAGGER_LOCALS=24
fly storm_1e5    1 100000
fly stagger_1e5  1 100000 ES_STAGGER_LOCALS=24

# 2. The table (worst bucket composition, frame_events, kick totals).
python3 - <<'EOF'
import json, re, glob, os
R = "lab/results/20261016-0504-system-e070/out"
def objs(p):
    txt = open(p).read(); dec = json.JSONDecoder(); i = 0; out = []
    while i < len(txt):
        while i < len(txt) and txt[i] != '{': i += 1
        if i >= len(txt): break
        o, j = dec.raw_decode(txt, i); out.append(o); i = j
    return out
for p in sorted(glob.glob(R + "/*.json")):
    o = objs(p); main = o[0]; an = [x for x in o if 'storm_anatomy' in x]
    kicks = int(re.search(r'kicks: (\d+)', main['stats']).group(1))
    fe = main['frame_events']
    w = an[0]['storm_anatomy']['worst'][1] if an else None   # worst non-birth bucket
    print(os.path.basename(p), dict(fe_max=fe['max'], fe_p99=fe['p99'], kicks=kicks,
         worst_bucket=(w or {}).get('events'), doll0=(w or {}).get('dolls', {}).get('0'),
         doll2=(w or {}).get('dolls', {}).get('2'),
         heaviest_tick=(w or {}).get('ticks_top', [[None]])[0][0]))
EOF
