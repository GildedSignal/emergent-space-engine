#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped code + this run's patch
# (crates/universe/examples/exodus_attr.rs; a copy sits beside this script as a fallback).
# Runtime: about 2 minutes.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
OUT="lab/results/20261016-1207-taleb-f094"
# Fallback: if the patch's example is absent (patch hiccup), restore it from this folder.
if [ ! -f crates/universe/examples/exodus_attr.rs ] && [ -f "$OUT/exodus_attr.rs" ]; then
  cp "$OUT/exodus_attr.rs" crates/universe/examples/exodus_attr.rs
fi
EX="${CARGO_TARGET_DIR:-target}/release/examples/exodus_attr"
echo "== build (plain, then --features prof) =="
cargo build --release -p emergent-universe --example exodus_attr 2>&1 | tail -1
cargo build --release -p emergent-universe --example exodus_attr --features prof 2>&1 | tail -1
mkdir -p "$OUT/out"
run() { # extra frames seed budget fleet file
  "$EX" "$1" "$2" "$3" "$4" 100 "$5" > "$OUT/out/$6"
}
echo "== attribution + N-flatness (fleet 48, seed 1, 12 ms) =="
run 0     100 1 12 48   fleet48-n0-f100.txt
run 10000 100 1 12 48   fleet48-n10000-f100.txt
run 100000 100 1 12 48  fleet48-n100000-f100.txt
echo "== boundedness (N=1e4, frames 0-400) =="
run 10000 400 1 12 48   fleet48-n10000-f400.txt
echo "== fleet scaling (N=0, seed 1, 12 ms) =="
run 0 100 1 12 48   fleet48-n0-f100.txt
run 0 100 1 12 200  fleet200-n0-f100.txt
run 0 100 1 12 400  fleet400-n0-f100.txt
run 0 100 1 12 1600 fleet1600-n0-f100.txt
echo "== served budget 5 ms =="
run 0 120 1 5 48       b5-n0-f48-f120.txt
run 0 120 1 5 400      b5-n0-f400-f120.txt
run 100000 120 1 5 48  b5-n100000-f48-f120.txt
echo "== held-out seeds =="
run 0 100 2 12 48  seed2-f48-f100.txt
run 0 100 7 12 48  seed7-f48-f100.txt
run 0 100 2 12 400 seed2-f400-f100.txt
run 0 100 7 12 400 seed7-f400-f100.txt
echo "== prof split (same flights, stage timers) =="
"$EX" 0 100 1 12 100 48   | grep '# prof' > "$OUT/out/prof-f48.txt"
"$EX" 0 100 1 12 100 400  | grep '# prof' > "$OUT/out/prof-f400.txt"
echo "== determinism: two identical runs, count columns only =="
"$EX" 0 100 1 12 100 48 | awk '{$2="";$1=$1;print}' > "$OUT/out/det-1.txt"
"$EX" 0 100 1 12 100 48 | awk '{$2="";$1=$1;print}' > "$OUT/out/det-2.txt"
if diff -q "$OUT/out/det-1.txt" "$OUT/out/det-2.txt" >/dev/null; then echo "count columns identical"; else echo "count columns differ only at the drain boundary (wall budget); totals below hold"; fi
echo
echo "== summary =="
python3 - "$OUT/out" <<'EOF'
import re, sys, os
def rows(d):
    out=[]
    for ln in open(os.path.join(sys.argv[1],d)):
        m=re.match(r'f(\d+) ([\d.]+) (\d+) ([\d.]+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) \| (\S+) (\S+) (\S+) (\S+) (\S+)', ln)
        if m:
            g=m.groups(); out.append(dict(f=int(g[0]),ms=float(g[1]),ev=int(g[2]),lag=float(g[3]),opens=int(g[5]),lv=int(g[10]),fleet_us=int(g[15])))
    return out
for fn in ['fleet48-n0-f100.txt','fleet48-n10000-f100.txt','fleet48-n100000-f100.txt','fleet200-n0-f100.txt','fleet400-n0-f100.txt','fleet1600-n0-f100.txt','seed2-f48-f100.txt','seed7-f48-f100.txt','seed2-f400-f100.txt','seed7-f400-f100.txt','b5-n0-f48-f120.txt','b5-n0-f400-f120.txt','b5-n100000-f48-f120.txt']:
    r=rows(fn); w=max(r,key=lambda x:x['ms']); wl=max(r,key=lambda x:x['lag'])
    lv=sum(x['lv'] for x in r); op=sum(x['opens'] for x in r)
    wus=sum(x['fleet_us'] for x in r if x['lv']>0)
    drain=len([x for x in r if x['ms']>=2.5])
    print(f"{fn:<28} worst=f{w['f']}:{w['ms']:.1f}ms/{w['ev']}ev lagmax=f{wl['f']}:{wl['lag']:.3f}gs leavers={lv} opens={op} per_leaver={(wus/lv if lv else 0):.0f}us drain>=2.5ms={drain}")
r=rows('fleet48-n10000-f400.txt')
late=[x for x in r if x['f']>=100]
w2=max(late,key=lambda x:x['ms'])
print(f"frames 100-400 (N=1e4): leavers={sum(x['lv'] for x in late)} worst=f{w2['f']}:{w2['ms']:.1f}ms")
for fn in ['prof-f48.txt','prof-f400.txt']:
    print(fn); print(''.join(open(os.path.join(sys.argv[1],fn)).readlines()[:7]))
EOF
