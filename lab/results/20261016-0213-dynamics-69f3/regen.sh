#!/bin/sh
# Regenerates every number in the dossier from shipped code + work/patch.diff.
# The patch is applied by the runner before this runs. Four arms in parallel, each ≤ 20 s.
set -e
cd "$(dirname "$0")/../../.."   # repo root
BIN=$(cargo build --release -p emergent-universe --example scanqueue --message-format=json 2>/dev/null | python3 -c "import json,sys
for l in sys.stdin:
    try: m=json.loads(l)
    except: continue
    if m.get('reason')=='compiler-artifact' and 'scanqueue' in m['target']['name']: print(m['executable'])")
D=lab/results/20261016-0213-dynamics-69f3
mkdir -p "$D/work"
cd "$D"
"$BIN" --n 500  --seed 1 --rtf 600 --burn-s 8 --coast-s 6 --warmup-s 2 > work/n500.jsonl     2> work/n500.err &
"$BIN" --n 1000 --seed 1 --rtf 600 --burn-s 8 --coast-s 6 --warmup-s 2 > work/pilot1000b.jsonl 2> work/pilot1000b.err &
"$BIN" --n 1000 --seed 7 --rtf 600 --burn-s 8 --coast-s 6 --warmup-s 2 > work/n1000s7.jsonl  2> work/n1000s7.err &
"$BIN" --n 2000 --seed 1 --rtf 600 --burn-s 8 --coast-s 6 --warmup-s 2 > work/n2000.jsonl    2> work/n2000.err &
wait
grep -h summary work/n500.err work/pilot1000b.err work/n1000s7.err work/n2000.err
python3 - <<'EOF'
import json
print("arm             S_ms  answers  pushes_burn  held_end  rss_end")
for name in ['n500','pilot1000b','n1000s7','n2000']:
    rows=[json.loads(l) for l in open(f'work/{name}.jsonl')]
    r=rows[-1]
    a,b=rows[120],rows[600]
    lam=(b['held']-a['held']+(b['answers']-a['answers']))/8
    print(f"{name:15s} {r['ans_ms']:5.2f} {r['answers']:6d}  {lam:10.2f}  {r['held']:7d}  {r['rss']:6.1f}")
EOF
