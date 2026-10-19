#!/usr/bin/env python3
"""Extinction analysis for the ringdown at n >= 6400 (second-author run ded5).

Instrument (fixed before the decisive runs, calibrated on the original 84b2 data):
- windows w64: sums of post-burn per-chronon contacts over 64-chronon windows;
- blocks: 32 windows = 2048 chronons, F64 per block (the 84b2 convention);
- whole-run m at a truncation H: relstd of w64 over post-burn chronons [0, H);
- late-m: relstd of w64 over the LAST `late` chronons of the post-burn series
  (default 4096 = the two final blocks; at 6400/H8192 this is the checker's
  "steady state" window, calibrated to read ~0.6%);
- T_early: 84b2's first-2048 spectral peak period.
Usage: late.py <csv>... [--late=N]
"""
import sys
import numpy as np


def series(f):
    rows, ticks = [], []
    for line in open(f):
        p = line.strip().split(",")
        if p[0] == "T":
            ticks.append(int(p[1]))
            rows.append(int(p[2]) if len(p) > 2 else 0)
    first = open(f).readline().split()
    meta = {k: v for k, v in zip(first[1::2], first[2::2])}
    a = np.array(rows, dtype=float)
    burn = int(meta.get("burn", "1024"))
    post = a[np.array(ticks) > burn]
    return meta, post


def w64(con):
    return np.add.reduceat(con, np.arange(0, len(con), 64))[: len(con) // 64]


fn = lambda s: s.var(ddof=1) / s.mean() if len(s) > 2 and s.mean() > 0 else float("nan")


def peak_period(seg):
    seg = seg - seg.mean()
    sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2
    sp[0] = 0
    i = int(np.argmax(sp))
    return (len(seg) // i if i else 0), (float(sp[i] / sp.sum()) if sp.sum() else 0.0)


def one(path, late=4096, truncs=(8192,)):
    meta, con = series(path)
    n, side = int(meta["n"]), int(meta["side"])
    out = {"file": path.split("/")[-1], "n": n, "side": side,
           "seed": meta["seed"], "H": len(con)}
    w = w64(con)
    nb = len(w) // 32
    out["blocks_F64"] = [round(fn(w[j * 32:(j + 1) * 32]), 1) for j in range(nb)]
    out["mean64"] = round(float(w.mean()), 1)
    out["m_whole"] = round(float(w.std(ddof=1) / w.mean() * 100), 2)
    out["F64_whole"] = round(fn(w), 2)
    out["identity"] = round(out["mean64"] * (out["m_whole"] / 100) ** 2, 2)
    lw = w64(con[-late:])
    out["m_late%d" % late] = round(float(lw.std(ddof=1) / lw.mean() * 100), 2)
    out["F64_late"] = round(fn(lw), 2)
    out["mean64_late"] = round(float(lw.mean()), 1)
    for H in truncs:
        if len(con) >= H:
            wt = w64(con[:H])
            out["m_trunc%d" % H] = round(float(wt.std(ddof=1) / wt.mean() * 100), 2)
            out["F64_trunc%d" % H] = round(fn(wt), 2)
            out["F1_trunc%d" % H] = round(float(con[:H].var(ddof=1) / con[:H].mean()), 3)
    out["F1_whole"] = round(float(con.var(ddof=1) / con.mean()), 3)
    out["p99p50_whole"] = round(float(np.percentile(con, 99) / np.percentile(con, 50)), 3)
    l8 = con[-8192:] if len(con) >= 8192 else con
    out["p99p50_late8k"] = round(float(np.percentile(l8, 99) / np.percentile(l8, 50)), 3)
    out["b0maxp50"] = round(float(w[:32].max() / np.percentile(w[:32], 50)), 3)
    wlat = w64(l8)
    out["latemaxp50"] = round(float(wlat.max() / np.percentile(wlat, 50)), 3)
    T, sh = peak_period(con[:2048])
    out["T_early"] = T
    out["sh_e"] = round(sh, 2)
    out["boxT"] = round(T / side, 1) if T else None
    return out


if __name__ == "__main__":
    args, late = [], 4096
    for a in sys.argv[1:]:
        if a.startswith("--late"):
            late = int(a.split("=")[1])
        else:
            args.append(a)
    for f in args:
        for k, v in one(f, late=late).items():
            print(f"   {k}: {v}")
        print()
