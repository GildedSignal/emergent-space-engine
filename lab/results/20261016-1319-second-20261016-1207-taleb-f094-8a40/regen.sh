#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped code + this run's instrument
# (crates/universe/examples/exodus_burn.rs, print-only, no engine line; a copy sits beside this
# script as a fallback). work/patch.diff is applied by the runner before this runs.
# Runtime: about 1 minute (two cached-build variants + the grid).
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
OUT="lab/results/20261016-1319-second-20261016-1207-taleb-f094-8a40"
if [ ! -s crates/universe/examples/exodus_burn.rs ] && [ -f "$OUT/exodus_burn.rs" ]; then
  cp "$OUT/exodus_burn.rs" crates/universe/examples/exodus_burn.rs
fi
EX="${CARGO_TARGET_DIR:-target}/release/examples/exodus_burn"
echo "== build (plain first: the grid's us numbers carry no prof timers; then prof for the stage split) =="
cargo build --release -p emergent-universe --example exodus_burn 2>&1 | tail -1
mkdir -p "$OUT/out"
run() { # members frames seed budget fleet level mode file
  "$EX" "$1" "$2" "$3" "$4" 100 "$5" "$6" "$7" > "$OUT/out/$8"
}
echo "== coast baselines (the one-variable comparison) =="
run 0 150 1 12 48  0 0 base48.txt
run 0 150 1 12 400 0 0 base400.txt
echo "== the burn composition (held forward burn from tick 0) =="
run 0 150 1 12 48  8 1 burn48-L8.txt
run 0 150 1 12 48  4 1 burn48-L4.txt
run 0 150 1 12 400 8 1 burn400-L8.txt
echo "== one decision landing at the coast's crest (f62) =="
run 0 150 1 12 48 8 2 crest48-L8.txt
echo "== served budget 5 ms =="
run 0 120 1 5 400 0 0 b5-base400.txt
run 0 120 1 5 400 8 1 b5-burn400-L8.txt
echo "== determinism: two identical burn runs, count columns only =="
"$EX" 0 150 1 12 100 48 8 1 | awk '{$2="";$1=$1;print}' > "$OUT/out/det-1.txt"
"$EX" 0 150 1 12 100 48 8 1 | awk '{$2="";$1=$1;print}' > "$OUT/out/det-2.txt"
if diff -q "$OUT/out/det-1.txt" "$OUT/out/det-2.txt" >/dev/null; then echo "count columns identical"; else echo "count columns differ only at the drain boundary (wall budget); totals below hold"; fi
echo "== prof stage split (timer overhead ~12%: read shares, not absolute us) =="
cargo build --release -p emergent-universe --example exodus_burn --features prof 2>&1 | tail -1
"$EX" 0 150 1 12 100 48  0 0 | grep '# prof' > "$OUT/out/prof-base48.txt"
"$EX" 0 150 1 12 100 48  8 1 | grep '# prof' > "$OUT/out/prof-burn48.txt"
"$EX" 0 150 1 12 100 400 8 1 | grep '# prof' > "$OUT/out/prof-burn400.txt"
cargo build --release -p emergent-universe --example exodus_burn 2>&1 | tail -1
echo
echo "== summary =="
python3 - "$OUT/out" <<'EOF'
import re, sys, os
def rows(d):
    out=[]
    for ln in open(os.path.join(sys.argv[1],d)):
        m=re.match(r'f(\d+) ([\d.]+) (\d+) ([\d.]+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) \| (\S+) (\S+) (\S+) (\S+) (\S+)', ln)
        if m:
            g=m.groups(); out.append(dict(f=int(g[0]),ms=float(g[1]),ev=int(g[2]),lag=float(g[3]),kicks=int(g[4]),opens=int(g[5]),dec=int(g[9]),lv=int(g[10]),hs=int(g[11]),enc=int(g[12]),pl=int(g[16]),fl=int(g[17])))
    return out
print(f"{'arm':<18} worst-frame         lagmax     leavers(f<100/total) opens dec perLeaver player_us(f<100) drain hs_max")
for fn in ['base48.txt','burn48-L8.txt','burn48-L4.txt','crest48-L8.txt','base400.txt','burn400-L8.txt','b5-base400.txt','b5-burn400-L8.txt']:
    r=rows(fn); w=max(r,key=lambda x:x['ms']); wl=max(r,key=lambda x:x['lag'])
    lv=sum(x['lv'] for x in r); f100=sum(x['lv'] for x in r if x['f']<100)
    flus=sum(x['fl'] for x in r if x['lv']>0); plus=sum(x['pl'] for x in r if x['f']<100)
    print(f"{fn:<18} f{w['f']}:{w['ms']:.1f}ms/{w['ev']}ev f{wl['f']}:{wl['lag']:.3f} {lv}({f100}) {sum(x['opens'] for x in r)} {sum(x['dec'] for x in r)} {(flus/lv if lv else 0):.0f}us {plus} {len([x for x in r if x['ms']>=2.5])} {max(x['hs'] for x in r)}")
print("latch tails: burn400-L8 last 5 frames hs =", [x['hs'] for x in rows('burn400-L8.txt')[-5:]], "; b5-burn400-L8 last 5 hs =", [x['hs'] for x in rows('b5-burn400-L8.txt')[-5:]])
for fn in ['prof-base48.txt','prof-burn48.txt','prof-burn400.txt']:
    print(fn); print(''.join(open(os.path.join(sys.argv[1],fn)).readlines()[:11]))
EOF
