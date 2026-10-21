#!/usr/bin/env python3
"""Adversarial instrument check: analyze.py's pooled stat tiles w~1400-1700 windows but
floors E[max] at min(w,512) windows (biased low). Redraw the pooled dues UNIFORMLY over the
same span, tile the SAME windows, and read max/mu. If the control also reads +0.25 excess,
the dossier's refutation is an artifact; if it reads ~0, the excess is real."""
import struct, sys
from pathlib import Path

def load(path):
    data = path.read_bytes(); out = {}; o = 0
    while o + 16 <= len(data):
        g, n, mn = struct.unpack_from("<IIq", data, o); o += 16
        gen = []
        for _ in range(n):
            i, off = struct.unpack_from("<Hq", data, o); o += 10
            gen.append((i, mn + off))
        out[g] = gen
    return out

def lcg(seed):
    st = [seed]
    def nxt():
        st[0] = (st[0] * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
        return st[0] >> 16
    return nxt

for seed in (1, 2):
    gens = load(Path(sys.argv[1]) / f"../dues_s{seed}.bin")
    gs = sorted(gens)
    seq = {}
    for g in gs:
        for i, d in gens[g]:
            seq.setdefault(i, {})[g] = d
    steps = []
    for i, s in seq.items():
        kk = sorted(s); iv = [s[k+1]-s[k] for k in kk[:-1]]
        if iv: steps.append(iv[len(iv)//2])
    steps.sort(); L = steps[len(steps)//2] // 32
    rng = lcg(0xC0FFEE + seed)
    for lo, hi in [(1,16),(17,48),(49,96),(97,gs[-1])]:
        dues = [d for g in gs if lo <= g <= hi for _, d in gens[g]]
        if len(dues) < 200: continue
        t0, t1 = min(dues), max(dues)
        w = max(1, (t1-t0)//L)
        def maxmu(ds):
            cnt = [0]*w
            for d in ds: cnt[min((d-t0)//L, w-1)] += 1
            mu = len(ds)/w
            return max(cnt)/mu, mu
        m_eng, mu = maxmu(dues)
        reps = 40
        ctrl = []
        for _ in range(reps):
            ds = [t0 + rng() % (t1-t0) for _ in dues]
            ctrl.append(maxmu(ds)[0])
        ctrl.sort()
        print(f"seed {seed} g[{lo},{hi}] w={w} mu={mu:.1f} engine max/mu={m_eng:.3f} "
              f"uniform-control(same geometry) median={ctrl[len(ctrl)//2]:.3f} "
              f"p10={ctrl[int(len(ctrl)*0.1)]:.3f} p90={ctrl[int(len(ctrl)*0.9)]:.3f} "
              f"true excess={m_eng-ctrl[len(ctrl)//2]:+.3f}")
