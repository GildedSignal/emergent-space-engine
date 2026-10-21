#!/usr/bin/env python3
"""Checker's pooled stat + same-geometry MT control for the two adversarial flights."""
import struct, random, sys
from pathlib import Path

def load(path):
    data = Path(path).read_bytes(); out = {}; o = 0
    while o + 16 <= len(data):
        g, n, mn = struct.unpack_from("<IIq", data, o); o += 16
        gen = []
        for _ in range(n):
            i, off = struct.unpack_from("<Hq", data, o); o += 10
            gen.append((i, mn + off))
        out[g] = gen
    return out

def bands(gens, tag):
    gs = sorted(gens)
    seq = {}
    for g in gs:
        for i, d in gens[g]: seq.setdefault(i, {})[g] = d
    steps = []
    for i, s in seq.items():
        kk = sorted(s); iv = [s[k+1]-s[k] for k in kk[:-1]]
        if iv: steps.append(iv[len(iv)//2])
    steps.sort(); L = steps[len(steps)//2] // 32
    rng = random.Random(99)
    last = gs[-1]
    cuts = [(1,16),(17,48),(49,96),(97,139),(140,200),(201,last)] if last > 200 else [(1,16),(17,48),(49,96),(97,last)]
    for lo, hi in cuts:
        if hi < lo: continue
        dues = [d for g in gs if lo <= g <= hi for _, d in gens[g]]
        if len(dues) < 200:
            continue
        t0, t1 = min(dues), max(dues); span = t1 - t0
        w = max(1, span // L)
        cnt = [0]*w
        for d in dues: cnt[min((d-t0)//L, w-1)] += 1
        mu = len(dues)/w; m_eng = max(cnt)/mu
        ctrl = []
        for _ in range(120):
            c = [0]*w
            for _ in range(len(dues)): c[rng.randrange(w)] += 1
            ctrl.append(max(c)/mu)
        ctrl.sort()
        # locked pairs in this flight's last full generation window set
        print(f"{tag} g[{lo},{hi}] n_g={len(gens[gs[0]])} w={w} mu={mu:.1f} engine={m_eng:.3f} "
              f"ctrl med={ctrl[len(ctrl)//2]:.3f} p90={ctrl[int(len(ctrl)*0.9)]:.3f} "
              f"excess={m_eng-ctrl[len(ctrl)//2]:+.3f} outside_p90={'YES' if m_eng > ctrl[int(len(ctrl)*0.9)] else 'no'}")

for tag, p in [("depth s1 g290", sys.argv[1]), ("big-N s1 n=11,700", sys.argv[2])]:
    fp = Path(p)
    if not fp.exists():
        print(f"{tag}: dump missing ({fp})"); continue
    bands(load(fp), tag)
