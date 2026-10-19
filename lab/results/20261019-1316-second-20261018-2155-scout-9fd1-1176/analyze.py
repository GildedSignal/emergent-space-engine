#!/usr/bin/env python3
"""Summarize the epoch-leak grid: pooled rows, the (1-1/E) law check, the
kappa/P laws, and the belt-real pricing readout. Run: python3 analyze.py"""
import csv, math, sys, io

BASE = __import__("os").environ.get("LABROOT", ".") + "/lab/results/20261019-1316-second-20261018-2155-scout-9fd1-1176"

def load(path):
    rows = []
    with open(path) as f:
        for r in csv.reader(l for l in f if not l.startswith("tag,")):
            if len(r) >= 12 and r[0] in ("grid", "grid16", "heldout", "dv0"):
                rows.append(dict(tag=r[0], E=r[1], P=int(r[2]), kap=r[3],
                                 pairs=int(r[4]), touches=int(r[5]), events=int(r[6]),
                                 misses=int(r[7]), rearms=int(r[8]), refresh=int(r[9]),
                                 lpt=float(r[10]), mf=float(r[11]) if r[11] != "nan" else float("nan")))
    return rows

def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 0.0)
    p = k / n; d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return (max(0.0, c-h), min(1.0, c+h))

def main():
    rows = load(f"{BASE}/grid.csv")
    out = io.StringIO()
    # pool seeds per (tag, E, P, kap)
    pool = {}
    for r in rows:
        key = (r["tag"], r["E"], r["P"], r["kap"])
        a = pool.setdefault(key, dict(events=0, misses=0, touches=0, refresh=0))
        a["events"] += r["events"]; a["misses"] += r["misses"]
        a["touches"] += r["touches"]; a["refresh"] += r["refresh"]
    out.write("== pooled (2 seeds) miss_frac vs the (1-1/E) law ==\n")
    out.write("tag      kap    P   E    events misses miss_frac  1-1/E   leak/touch  CI95(lo,hi)\n")
    for key in sorted(pool, key=lambda k: (k[0], float(k[3]), k[2], int(k[1]) if k[1]!="noarm" else 0)):
        a = pool[key]
        tag, E, P, kap = key
        try: Ei = int(E)
        except: Ei = 10**9
        mf = a["misses"]/a["events"] if a["events"] else float("nan")
        pred = 1 - 1/Ei if Ei < 10**6 else 1.0
        lo, hi = wilson(a["misses"], a["events"]) if a["events"] else (0,0)
        out.write(f"{tag:8s} {kap:>5s} {P:3d} {E:>5s} {a['events']:7d} {a['misses']:6d} "
                  f"{mf:9.4f} {pred:7.4f} {a['misses']/a['touches']:11.3e}  ({lo:.3f},{hi:.3f})\n")
    # kappa-law: event rate per touch at E=2 (near-pure leak), per P
    out.write("\n== event rate per touch (kappa-law; events/touches) ==\n")
    for P in (1, 4, 16):
        for kap in ("1e-8", "1e-7", "6e-5"):
            for tag in ("grid", "grid16"):
                a = pool.get((tag, "2", P, kap))
                if a:
                    out.write(f"P={P:2d} kap={kap:>5s}: {a['events']/a['touches']:.3e} events/touch\n")
                    break
    # P-law at quantum
    out.write("\n== P-law at kap=1e-7 (E=2): events/touch ratio ==\n")
    base = None
    for P in (1, 4, 16):
        for tag in ("grid", "grid16"):
            a = pool.get((tag, "2", P, "1e-7"))
            if a:
                r_ = a["events"]/a["touches"]
                if P == 1: base = r_
                out.write(f"P={P:2d}: {r_:.3e}" + (f"  ratio {r_/base:.2f}" if base else "") + "\n")
                break
    # belt-real pricing
    out.write("\n== belt-real pricing (P=4, quantum, E>=64 pooled) ==\n")
    a = pool.get(("grid", "64", 4, "1e-7"))
    if a:
        lpt = a["misses"]/a["touches"]
        out.write(f"leak/touch {lpt:.3e}; per cand per CELL kick (x2/n, n=2000): {lpt*1e-3:.3e}\n")
        out.write(f"budget 1a29 eps=1e-6: margin {1e-6/(lpt*1e-3):.0f}x\n")
        for E_pair in (256, 1024):
            E_cell = 1000*E_pair
            out.write(f"E_pair={E_pair}: E_cell={E_cell:.0e} -> 355-core row {355/E_cell:.1e} cores\n")
    print(out.getvalue())

if __name__ == "__main__":
    main()
