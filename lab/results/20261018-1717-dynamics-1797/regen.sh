#!/bin/sh
# Regenerates every number in dossier.md from shipped code + work/patch.diff.
# Total: one cargo build (~2-3 min cold) + ~15 s of runs + ~5 s analysis. Well under 15 min.
set -e
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261018-1717-dynamics-1797

# 1. Apply the probe (a new example on shipped pub APIs; touches no engine line).
if git apply --check "$R/work/patch.diff" 2>/dev/null; then git apply "$R/work/patch.diff"; else echo "patch already applied"; fi

# 2. The decisive deep run: 8 arms x 65536 (three capped at 16384, one at 4096) chained
#    seam crossings; per-crossing columns as JSONL. ~7 s.
cargo run --release -q -p emergent-space --example circle_ratchet -- 65536 > "$R/deep.jsonl" 2>"$R/deep.err"

# 3. The anchor control run (adds the e=0.5 exact-translation arm): ~5 s.
cargo run --release -q -p emergent-space --example circle_ratchet -- 4096 > "$R/control.jsonl" 2>/dev/null

# 4. Analysis: table, diffusion fit D^2=2Cn, rate(D) collapse, price, w census.
python3 "$R/analyze.py" "$R/deep.jsonl" > "$R/analysis.txt" 2>&1
python3 - "$R/control.jsonl" <<'EOF' >> "$R/analysis.txt"
import json, sys
from collections import Counter
rows=[json.loads(l) for l in open(sys.argv[1])]
a=[r for r in rows if r['arm']=='p21_e5_phi38']
dk=[r['k2']-r['k'] for r in a]
print("\n== anchor control: e=0.5 p=2^21 phi=3/8 (record: exactly -13) ==")
print("depth", len(dk), "census:", Counter(dk).most_common(3))
b=[r for r in rows if r['arm']=='p21_em3_phi1']
print("anchor control: e=1e-3 p=2^21 phi=1/8 (record: exactly -1):", Counter(r['k2']-r['k'] for r in b).most_common(3))
EOF
python3 - "$R/deep.jsonl" <<'EOF' >> "$R/analysis.txt"
import json, math, sys
UNIT=1<<48
rows=[json.loads(l) for l in open(sys.argv[1])]
arms={}
for r in rows: arms.setdefault(r['arm'],[]).append(r)
print("\n== D^2 vs n linearity + w drift census (dossier table) ==")
for arm,a in arms.items():
    if 'em3' in arm: continue
    pts=[(i+1, UNIT-a[i]['k2']) for i in range(0,len(a),max(1,len(a)//64))]
    xs=[p[0] for p in pts]; ys=[p[1]**2 for p in pts]
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    sxx=sum((x-mx)**2 for x in xs); sxy=sum((x-mx)*(y-my) for x,y in zip(xs,ys)); syy=sum((y-my)**2 for y in ys)
    C=sxy/sxx/2; r2=sxy*sxy/(sxx*syy)
    dw=[]
    for r in a:
        x=((r['w2']-r['w'])%2**32)/2**32
        dw.append(x-1.0 if x>0.5 else x)
    drift=sum(dw)/len(dw); neg=100*sum(1 for x in dw if x<0)/len(dw)
    jumps=sum(1 for x in dw if abs(x)>1e-2)
    print(f"{arm:18s} C={C:.3e} R2={r2:.6f}  w_drift={drift:+.2e}/cross (neg {neg:.0f}%, jumps>1e-2: {jumps}, max|dw| {max(abs(x) for x in dw):.3f})")
    if 'e0_phi1' == arm[4:11] or arm=='p21_e0_phi1':
        Dstar=0.01*UNIT; n1=C/2
        print(f"  price: n(sqrt to floor)={n1:.2e}; composite n*(D*=1%k) ~ {n1 + (Dstar-C):.2e}")
EOF
# 5. Keep the archived record under 5 MB: subsample the raw series, drop the big files
#    (regenerable in ~12 s by this script).
python3 - "$R" <<'EOF_SUB'
import gzip, collections, sys, os
R=sys.argv[1]
def subsample(src, dst, stride=128, head=256):
    arms=collections.defaultdict(list)
    for l in open(src): arms[l.split('"')[3]].append(l)
    with gzip.open(dst,'wt') as f:
        for arm, ls in arms.items():
            for l in ls[:head] + ls[head::stride]: f.write(l)
subsample(os.path.join(R,'deep.jsonl'), os.path.join(R,'deep-sample.jsonl.gz'))
subsample(os.path.join(R,'control.jsonl'), os.path.join(R,'control-sample.jsonl.gz'), stride=8, head=512)
for f in ('deep.jsonl','control.jsonl'): os.remove(os.path.join(R,f))
EOF_SUB
cat "$R/analysis.txt"
echo "REGEN DONE"
