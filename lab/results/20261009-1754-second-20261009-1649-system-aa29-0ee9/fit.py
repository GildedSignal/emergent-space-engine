#!/usr/bin/env python3
"""Fit per-order gate constants and the LOCK threshold from CALIBRATION runs only.

Label (what the kick layer must not miss, on non-chaotic seeds):
  FAIL_pump = pump > 2.5 x local (+-0.12 in alpha) 20th-percentile baseline
  LOCK      = lockR >= LOCK_THR (circular judge, no detrend; -1 if < 5 flips)
  chaos     = a_drift > 0.05 (excluded; owned by the dense tier)
  label_pos = FAIL_pump or LOCK

Detector: FLAG iff some CF convergent p/q (q<=12, order=p-q in 1..4) has
q|alpha - p/q| < K_order. Fit: K_order = max gate coordinate x = q|alpha-p/q|
over label_pos seeds whose NEAREST convergent (min dN1) has that order, pooled
over the calibration runs. Zero calibration misses by construction; the cost is
the FP count, reported with the fit.

Usage: python3 fit.py RUN.json ...   (prints per-order fit + sharpness table)
"""
import json, sys
import numpy as np

LOCK_THR = 0.90
BASE_WIN = 0.12
BASE_FACTOR = 2.5


def load(path):
    d = json.load(open(path))
    rows = d["rows"]
    al = np.array([r["alpha"] for r in rows])
    pu = np.array([r["pump"] for r in rows])
    base = np.empty(len(al))
    for i, a in enumerate(al):
        sel = np.abs(al - a) <= BASE_WIN
        base[i] = np.percentile(pu[sel], 20) if sel.sum() >= 8 else np.percentile(pu, 20)
    for i, r in enumerate(rows):
        r["fail"] = bool(pu[i] > BASE_FACTOR * base[i])
        r["chaos"] = bool(r["a_drift"] > 0.05)
        r["lock"] = bool(r["lockR"] >= LOCK_THR)
        r["pos"] = (r["fail"] or r["lock"]) and not r["chaos"]
        r["x"] = r["q"] * r["dist"] if r.get("q") else 9.9
    return d["meta"], rows


def main(paths):
    allrows = []
    for p in paths:
        meta, rows = load(p)
        nc = sum(1 for r in rows if not r["chaos"])
        print(f"{p}: mu={meta['mu']:.0e} e0={meta['e0']} [{meta['amin']}-{meta['amax']}] "
              f"n={len(rows)} chaos={len(rows)-nc} pos={sum(r['pos'] for r in rows)} "
              f"(fail={sum(r['fail'] and not r['chaos'] for r in rows)}, "
              f"lock={sum(r['lock'] and not r['chaos'] for r in rows)})")
        allrows += rows
    print(f"\nLOCK threshold = {LOCK_THR}")
    print("\nPer-order fit (pooled calibration, nearest convergent by dN1):")
    for o in (1, 2, 3, 4):
        rs = [r for r in allrows if r.get("order") == o and not r["chaos"]]
        pos = [r for r in rs if r["pos"]]
        if not rs:
            print(f"  order {o}: no seeds")
            continue
        xs = np.array([r["x"] for r in rs])
        xpos = np.array([r["x"] for r in pos]) if pos else np.array([])
        K = xpos.max() if len(xpos) else 0.0
        npos = len(pos)
        # sharpness: label fraction in bins of x/K
        bins = [0, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 1e9]
        frac = []
        for lo, hi in zip(bins[:-1], bins[1:]):
            m = (xs * (1.0 / max(K, 1e-9)) >= lo) & (xs * (1.0 / max(K, 1e-9)) < hi)
            lbl = np.array([r["pos"] for r in rs])
            frac.append(f"{lbl[m].mean():.2f}({m.sum()})" if m.sum() else "-")
        print(f"  order {o}: n={len(rs)} pos={npos} K={K:.4f} "
              f"pos-by-x/K bins {[f'{b:g}' for b in bins[:-1]]}: {' '.join(frac)}")
        # breakdown by e0
        for e0 in sorted({r['e0'] for r in rs} if 'e0' in rs else set()):
            pass
    # per-run per-order max x of pos (e0 dependence)
    print("\nPer-run K_o candidates (max x over pos, nearest order):")
    for p in paths:
        meta, rows = load(p)
        line = []
        for o in (1, 2, 3, 4):
            xs = [r["x"] for r in rows if r.get("order") == o and r["pos"]]
            line.append(f"o{o}={max(xs):.4f}" if xs else f"o{o}=--")
        print(f"  {p} (e0={meta['e0']}): " + " ".join(line))
    # lock value distribution at order-1 interiors vs flanks
    print("\nlockR by x-band, order-1 nearest, non-chaotic (pooled):")
    rs = [r for r in allrows if r.get("order") == 1 and not r["chaos"]]
    for lo, hi in [(0, 0.02), (0.02, 0.05), (0.05, 0.08), (0.08, 0.12), (0.12, 0.3), (0.3, 9)]:
        m = [r for r in rs if lo <= r["x"] < hi]
        if m:
            lr = np.array([r["lockR"] for r in m])
            print(f"  x in [{lo},{hi}): n={len(m)} lockR med={np.median(lr):.2f} "
                  f"q90={np.quantile(lr, 0.9):.2f} frac>=0.9={np.mean(lr >= 0.9):.2f} "
                  f"failfrac={np.mean([r['fail'] for r in m]):.2f}")


if __name__ == "__main__":
    main(sys.argv[1:])
