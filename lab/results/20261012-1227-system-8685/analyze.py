#!/usr/bin/env python3
"""Analyze window_clock CSVs: ensemble behaviour scores vs truth, per config."""
import csv, math, os, statistics as st

W = os.path.join(os.path.dirname(os.path.abspath(__file__)), "work")

def load(name):
    rows = []
    with open(os.path.join(W, name)) as f:
        for r in csv.DictReader(f):
            rows.append({k: (r[k] if k in ("config","variant") else (int(float(v)) if k in ("seed","kicks","solves","ejected_at_sample","nfit") else float(v))) for k, v in r.items()})
    return rows

def med(x): return st.median(x) if x else float("nan")
def mad(x):
    if not x: return float("nan")
    m = med(x)
    return med([abs(v - m) for v in x])

BODY_ORBITS = {"encounter": 1000 * 2*math.pi / (2*math.pi*1.25**1.5),
               "resonant":  1000 * 2*math.pi / (2*math.pi*1.5874**1.5),
               "belt":      500 * 5.2**1.5}

VARIANTS = ["u64","u32","u16","u8","w0.25","w0.5","w1.0","w0.5seg8"]

for cfg in ["encounter","resonant","belt"]:
    truth = load(f"{cfg}-truth.csv")
    tv = [r["varpi_rate"] for r in truth if r["nfit"] > 0]
    te = [r["e_rate"] for r in truth if r["nfit"] > 0]
    tj = [r["jacobi_max"] for r in truth]
    print(f"\n=== {cfg} (body orbits in run: {BODY_ORBITS[cfg]:.0f}) ===")
    print(f"truth u2048: med wpidot={med(tv):.3e} MAD={mad(tv):.3e}  med edot={med(te):.3e} MAD={mad(te):.3e} "
          f"eject={sum(1 for r in truth if r['ejected_at_sample']>=0)}  med JacobiMax={med(tj):.3e}")
    # truth convergence check
    for fine in [f"{cfg}-truthfine"]:
        if os.path.exists(os.path.join(W, fine + ".csv")):
            tf = load(fine + ".csv")
            fv = [r["varpi_rate"] for r in tf if r["nfit"] > 0]
            fe = [r["e_rate"] for r in tf if r["nfit"] > 0]
            if fv:
                dz = abs(med(fv) - med(tv)) / (mad(tv) + 1e-30)
                de = abs(med(fe) - med(te)) / (mad(te) + 1e-30)
                print(f"  truth check u4096 (4 seeds): dmed(wpidot)={dz:.2f} MADs, dmed(edot)={de:.2f} MADs")
    print(f"{'variant':<10} {'kicks/orbit':>11} {'d_wpidot(MAD)':>13} {'d_edot(MAD)':>12} {'Deject':>6} {'medJacMax':>10}")
    for v in VARIANTS:
        rows = load(f"{cfg}-{v}.csv")
        kv = [r["varpi_rate"] for r in rows if r["nfit"] > 0]
        ke = [r["e_rate"] for r in rows if r["nfit"] > 0]
        kj = [r["jacobi_max"] for r in rows]
        kpo = sum(r["kicks"] for r in rows) / len(rows) / BODY_ORBITS[cfg]
        eject = sum(1 for r in rows if r["ejected_at_sample"] >= 0)
        dw = abs(med(kv) - med(tv)) / (mad(tv) + 1e-30) if kv else float("nan")
        de = abs(med(ke) - med(te)) / (mad(te) + 1e-30) if ke else float("nan")
        print(f"{v:<10} {kpo:>11.2f} {dw:>13.2f} {de:>12.2f} {eject:>6} {med(kj):>10.3e}")
