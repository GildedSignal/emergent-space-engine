#!/usr/bin/env python3
"""Summary table for dossier.md: the Fano identity, block decay, periods, allocator ratios."""
import numpy as np, glob, os, collections

def series(f):
    T = []
    for line in open(f):
        p = line.strip().split(",")
        if p[0] == 'T': T.append([int(x) if x else 0 for x in p[1:]])
    tk = open(f).readline().split()
    meta = {k: v for k, v in zip(tk[1::2], tk[2::2])}
    T = np.array(T)
    burn = int(meta.get("burn", "1024"))
    return int(meta["n"]), int(meta["side"]), T[T[:,0] > burn, 1].astype(float)

def w64(con):
    return np.add.reduceat(con, np.arange(0, len(con), 64))[:len(con)//64]

fn = lambda s: s.var(ddof=1)/s.mean()

def blocks(w, nbl=4):
    return [round(fn(w[j*32:(j+1)*32]), 1) for j in range(min(nbl, len(w)//32))]

def peak(seg):
    seg = seg - seg.mean()
    sp = np.abs(np.fft.rfft(seg*np.hanning(len(seg))))**2; sp[0] = 0
    i = int(np.argmax(sp)); return i, sp[i]/sp.sum()

print("== N-ladder (fill 0.7, vmax 2^16, burn 1024, horizon 8192) ==")
print(f"{'n':>6} {'side':>4} {'F1':>10} {'F64':>16} {'mean64':>8} {'m=relsd64':>16} {'identity':>9} {'p99/p50':>8} {'b0max/p50':>9} {'T_early':>7} {'sh_e':>5} {'blocks(s1)':>28}")
by = collections.defaultdict(list)
for f in sorted(glob.glob('data/lad_n*_s*.csv')):
    n, side, con = series(f)
    if len(con) < 8000: continue
    by[n].append((f, side, con))
for n in sorted(by):
    rows = by[n]
    F1s = [fn(con) for _, _, con in rows]
    ws = [w64(con) for _, _, con in rows]
    F64s = [fn(w) for w in ws]
    m = float(np.mean([w.std(ddof=1)/w.mean() for w in ws]))
    f0, side, con = rows[0]
    w = w64(con)
    i, sh = peak(con[:2048])
    T = 2048//i if i else 0
    print(f"{n:6d} {side:4d} {min(F1s):5.2f}-{max(F1s):4.2f} {min(F64s):5.2f}-{max(F64s):5.2f} {w.mean():8.0f} {m*100:15.2f}% {w.mean()*m*m:9.2f} {np.percentile(con,99)/np.percentile(con,50):8.3f} {w[:32].max()/np.percentile(w[:32],50):9.3f} {T:7d} {sh:5.2f} {str(blocks(w)):>28}")

print("\n== Dephasing at n = 6400 (seed 1; control = lad_n6400_s1) ==")
for f in ['data/lad_n6400_s1.csv', 'data/poly_m6400_s1.csv', 'data/poly_r6400_s1.csv']:
    if not os.path.exists(f): print(f"{f}: missing"); continue
    n, side, con = series(f)
    w = w64(con)
    i, sh = peak(con[:2048])
    print(f"{os.path.basename(f):20s} F64 {fn(w):7.2f} mean64 {w.mean():8.0f} m {w.std(ddof=1)/w.mean()*100:5.2f}% b0max/p50 {w[:32].max()/np.percentile(w[:32],50):5.3f} T {2048//max(i,1):5d} sh {sh:4.2f} blocks {blocks(w)}")

print("\n== Long horizons: does the ringdown return? (late 8192 chronons) ==")
for f in sorted(glob.glob('data/long_*.csv')):
    if not os.path.exists(f): continue
    n, side, con = series(f)
    if len(con) < 16384: print(f"{os.path.basename(f):20s} partial {len(con)}"); continue
    w = w64(con)
    nb = len(w)//32
    tail = [round(fn(w[j*32:(j+1)*32]), 1) for j in range(nb-4, nb)]
    mx = max(wp.max()/np.percentile(wp, 50) for wp in [w[j*32:(j+1)*32] for j in range(nb)])
    print(f"{os.path.basename(f):20s} horizon {len(con)} last-block F64 {tail} whole-run w64 max/p50 {mx:.3f}")
