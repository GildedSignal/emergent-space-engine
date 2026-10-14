#!/usr/bin/env bash
# Regen for 20261014-1010-quant-036c: every dossier number, from the patch in work/patch.diff
# (applied by the runner before this runs). ~6 min on a shared 8-vCPU Linux box, well under 15.
set -euo pipefail
cd "$(dirname "$0")/../../.."        # repo root (lab/results/<id>/ is 3 below it)
W=lab/results/20261014-1010-quant-036c/work
mkdir -p "$W/arms"
run() { cargo run --release -p xtask --features prof -- universe "$@"; }

echo "== kick-bench arms (one prof binary, off = shipped, on = ES_IMPACT_GUESS=1)"
for arm in "4000 3 1 3" "1500 3 1 3" "1500 7 1 3" "400 3 100 3"; do
  set -- $arm
  for g in 0 1; do
    n="$W/arms/kb-m$1-seed$2-rtf$3-$([ $g = 1 ] && echo on || echo off).json"
    if [ "$g" = 1 ]; then ES_IMPACT_GUESS=1 ES_MEMBERS=4096 run --kick-bench --seed "$2" --rtf "$3" --seconds "$4" --members "$1" > "$n"
    else ES_MEMBERS=4096 run --kick-bench --seed "$2" --rtf "$3" --seconds "$4" --members "$1" > "$n"; fi
  done
done

echo "== bench arms (plain build, no prof) + pristine digest control"
bench() { cargo run --release -p xtask -- universe "$@"; }
ES_MEMBERS=4096 bench --bench --seed 3 --rtf 1 --seconds 8 --members 4000 > "$W/arms/bench-m4000-s8-off.json"
ES_IMPACT_GUESS=1 ES_MEMBERS=4096 bench --bench --seed 3 --rtf 1 --seconds 8 --members 4000 > "$W/arms/bench-m4000-s8-on.json"
ES_MEMBERS=4096 bench --kick-bench --seed 3 --rtf 1 --seconds 3 --members 1500 > "$W/arms/kb-m1500-pristine.json"

echo "== suite with the guess forced on"
ES_IMPACT_GUESS=1 cargo test --release -p emergent-universe --tests 2>&1 | grep -E "^(test result|error)" 

echo "== summary (digests must match within each arm pair; us/call is the search)"
python3 - <<'EOF'
import json, glob, os
W = os.path.join(os.path.dirname(__file__) if '__file__' in dir() else '.', '')
W = 'lab/results/20261014-1010-quant-036c/work/arms'
for pre in ['kb-m4000-seed3-rtf1', 'kb-m400-seed3-rtf100', 'kb-m1500-seed3-rtf1', 'kb-m1500-seed7-rtf1']:
    o = json.load(open(f'{W}/{pre}-off.json')); n = json.load(open(f'{W}/{pre}-on.json'))
    ok = 'IDENTICAL' if o['digest'] == n['digest'] and o['replay_digest'] == n['replay_digest'] else 'DIGEST MOVED'
    print(f"{pre}: made {o['kick_us']['median']:.1f}->{n['kick_us']['median']:.1f}  leavers {o['kick_us_leavers']['median']:.1f}->{n['kick_us_leavers']['median']:.1f}  "
          f"search {o['prof_impact']['us_per_call']:.1f}->{n['prof_impact']['us_per_call']:.1f} us/call  guess_share {n['prof_impact']['guess_share']:.2f}  {ok}")
b = [json.load(open(f'{W}/bench-m4000-s8-{a}.json')) for a in ('off', 'on')]
print(f"bench m4000/s8: digest {b[0]['digest'][:16]} vs {b[1]['digest'][:16]} ({'IDENTICAL' if b[0]['digest']==b[1]['digest'] else 'MOVED'})")
p = json.load(open(f'{W}/kb-m1500-pristine.json')); q = json.load(open(f'{W}/kb-m1500-seed3-rtf1-off.json'))
print(f"pristine vs prof-off digest: {p['digest'][:16]} vs {q['digest'][:16]} ({'IDENTICAL' if p['digest']==q['digest'] else 'MOVED'})")
EOF
