#!/usr/bin/env python3
"""Breathing-mode analysis: Fano ladder, spectrum, mode shape, decay, dephasing."""
import sys, glob
import numpy as np

KEYS = ("n","fill","phi","side","per_row","cell","vmax","seed","burn","horizon","keep",
        "contacts","walls","distinct_pairs","bodies_hit","mean|k|","maxdisp_lc","ops","maxbatch","masses","radii")

def load(path):
    meta, T, V = {}, [], []
    for line in open(path):
        p = line.strip().split(",")
        if not p[0].startswith("#"):
            if p[0] == "T":
                T.append([int(x) if x else 0 for x in p[1:]])
            elif p[0] == "V":
                V.append([int(x) for x in p[1:]])
            continue
        toks = line.split()
        if len(toks) > 2 and toks[1] == "end":
            it = iter(toks[2:])
            for k in it:
                if k in KEYS:
                    try: meta[k] = next(it)
                    except StopIteration: pass
            continue
        if len(toks) > 2 and toks[1] in KEYS:
            it = iter(["n"] + toks[2:]) if toks[1] == "n" else iter(toks[1:])
            for k in it:
                if k in KEYS:
                    try: meta[k] = next(it)
                    except StopIteration: pass
    return meta, (np.array(T) if T else np.empty((0,0))), (np.array(V, dtype=float) if V else np.empty((0,0)))

def fano(x, w):
    s = np.add.reduceat(x, np.arange(0, len(x), w))[:len(x)//w]
    return s.var(ddof=1)/s.mean() if len(s) > 2 and s.mean() > 0 else float("nan")

def win(x, w):
    return np.add.reduceat(x, np.arange(0, len(x), w))[:len(x)//w]

def spectrum(x, top=6, share=0.02):
    x = x - x.mean()
    if len(x) < 256: return []
    p = np.abs(np.fft.rfft(x * np.hanning(len(x))))**2
    p[0] = 0
    tot = p.sum()
    if tot <= 0: return []
    idx = np.argsort(p)[::-1][:top]
    return [(round(i/len(x), 7), round(p[i]/tot, 3)) for i in sorted(idx) if p[i]/tot > share]

def stats(path):
    meta, T, V = load(path)
    if len(T) == 0: return None
    burn = int(meta.get("burn", 0)); n = int(meta.get("n", 0))
    post = T[T[:,0] > burn]
    con = post[:,1].astype(float)
    r = {
        "n": n, "seed": meta.get("seed","?"), "phi": meta.get("phi","?"), "cell": meta.get("cell","?"),
        "side": meta.get("side","?"), "masses": meta.get("masses","[1]"), "radii": meta.get("radii","[1.0]"),
        "nu": round(con.mean()/n, 5) if n else None,
        "F1": round(con.var(ddof=1)/con.mean(), 3),
        "F8": round(fano(con, 8), 2), "F64": round(fano(con, 64), 2), "F512": round(fano(con, 512), 2),
        "p99p50": round(np.percentile(con,99)/np.percentile(con,50), 3),
        "w64p99p50": round(np.percentile(win(con,64),99)/np.percentile(win(con,64),50), 3) if len(con)>=256 else None,
        "w64maxp50": round(win(con,64).max()/np.percentile(win(con,64),50), 3) if len(con)>=256 else None,
        "spec": spectrum(con),
        "maxdisp": meta.get("maxdisp_lc",""), "dpairs": meta.get("distinct_pairs",""), "maxbatch": meta.get("maxbatch",""),
    }
    if len(con) >= 1024:
        e = win(con, 64)
        r["mean64"] = round(e.mean(), 1)
        r["relstd64"] = round(e.std(ddof=1)/e.mean(), 4)
        env = win(con, 512)
        r["env512_min/max"] = round(env.min()/env.max(), 3)
        x = (con - con.mean())/con.std()
        x4096 = x[:4096]
        ac = np.correlate(x4096, x4096, "full")[len(x4096)-1:]
        ac /= ac[0]
        lag = int(np.argmax(np.abs(ac[8:4096])) + 8)
        r["ac_peak_lag"] = lag
        r["ac_peak_val"] = round(float(ac[lag]), 3)
        r["ac_lag2048"] = round(float(ac[min(2048, len(ac)-1)]), 3)
    if len(con) >= 2048:
        r["spec_early"] = spectrum(con[:2048], top=4, share=0.03)
        r["spec_late"] = spectrum(con[-2048:], top=4, share=0.03)
    if post.shape[1] >= 11:
        xb = post[:,3:11].astype(float)
        c = np.corrcoef(xb.T)
        r["bandcorr"] = round(((c.sum() - np.trace(c))/56), 3)
        r["LRcorr"] = round(np.corrcoef(xb[:,:4].sum(1), xb[:,4:].sum(1))[0,1], 3)
        sp = r["spec"]
        if sp:
            fp = sp[0][0]
            t = post[:,0].astype(float)
            r["bandphase"] = [round(np.angle(np.exp(-2j*np.pi*fp*t) @ xb[:,i]), 2) for i in range(8)]
    if len(V) > 64 and V.shape[1] == 17:
        vx = V[V[:,0] > burn, 1:9]
        r["vpeak"] = [spectrum(vx[:,i])[0][0] if spectrum(vx[:,i]) else None for i in range(8)][:4]
    return r

if __name__ == "__main__":
    files = sys.argv[1:]
    for f in files:
        r = stats(f)
        if r:
            print(f":: {f}")
            for k, v in r.items(): print(f"   {k}: {v}")
