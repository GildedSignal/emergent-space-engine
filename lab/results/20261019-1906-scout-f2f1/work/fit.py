#!/usr/bin/env python3
"""Fit the closed form for the epoch-rule leak curve (encounters od 3).

Model: an event at arm-offset j is caught iff the book (scheduled due) has
survived j kicks; survival S_j = w*r1**j + (1-w)*r2**j (geometric = w=0).
miss_frac(E) = 1 - (1/E) * sum_{j<E} S_j   [events uniform over offsets,
measured: E=2 census j0 138 ev / j1 130 ev].
Leak per touch: leak(E) = h * miss_frac(E), h the arm-coupled event rate.

Fit per (P, kappa) arm by binomial-likelihood over pooled seeds; jackknife:
fit on E <= 8, predict E in {16, 64, 256, 1024}.
"""
import csv, math, sys, glob, re
from itertools import product

def load(path):
    arms = {}
    for row in csv.DictReader(open(path)):
        if row["tag"] != "law":
            continue
        key = (int(row["P"]), float(row["kappa"]))
        if not row["E"].isdigit():
            continue
        E = int(row["E"])
        if E > 1024:
            continue
        d = arms.setdefault(key, {})
        p = d.setdefault(E, [0, 0])
        p[0] += int(row["events"]); p[1] += int(row["misses"])
    return arms

def mf_model(E, w, r1, r2):
    s = sum(w * r1**j + (1 - w) * r2**j for j in range(E))
    return 1.0 - s / E

def nll(theta, data):
    w, r1, r2 = theta
    if not (0 <= w <= 1 and 0 <= r1 <= 1 and 0 <= r2 <= 1):
        return float("inf")
    n = 0.0
    for E, (ev, miss) in data.items():
        m = min(max(mf_model(E, w, r1, r2), 1e-9), 1 - 1e-9)
        n -= miss * math.log(m) + (ev - miss) * math.log(1 - m)
    return n

def fit(data, fit_Es):
    sub = {E: v for E, v in data.items() if E in fit_Es}
    best = (float("inf"), None)
    # coarse grid + local refine (no scipy dependency)
    for w in [0.0, 0.25, 0.5, 0.75, 1.0]:
        for r1 in [i / 20 for i in range(21)]:
            for r2 in [i / 20 for i in range(21)]:
                v = nll((w, r1, r2), sub)
                if v < best[0]:
                    best = (v, (w, r1, r2))
    (w, r1, r2), step = best[1], 0.05
    while step > 1e-4:
        improved = True
        while improved:
            improved = False
            for dw, dr1, dr2 in product([-step, 0, step], repeat=3):
                t = (min(max(w + dw, 0), 1), min(max(r1 + dr1, 0), 1), min(max(r2 + dr2, 0), 1))
                v = nll(t, sub)
                if v < best[0] - 1e-12:
                    best, improved = (v, t), True
                    w, r1, r2 = t
        step /= 2
    return best[1]

def main():
    arms = {}
    for f in glob.glob(sys.argv[1] if len(sys.argv) > 1 else "work/law_*.csv"):
        for k, v in load(f).items():
            arms.setdefault(k, {})
            for E, p in v.items():
                q = arms[k].setdefault(E, [0, 0])
                q[0] += p[0]; q[1] += p[1]
    print("arm (P,kappa) | pooled events | fit on E<=8: w,r1,r2 | predict E=16/64/256/1024 (meas)")
    for key in sorted(arms):
        data = arms[key]
        if 1 not in data or data[1][1] != 0:
            print(key, "E1 control not clean, skip"); continue
        ev_tot = data[max(data)][0]
        th = fit(data, {2, 4, 8})
        line = f"P={key[0]:<3} kap={key[1]:.0e} ev={ev_tot:<4} fit w={th[0]:.3f} r1={th[1]:.3f} r2={th[2]:.3f} |"
        for E in (16, 64, 256, 1024):
            if E in data:
                ev, miss = data[E]
                line += f" {mf_model(E, *th):.3f}/{miss/ev:.3f}"
        print(line)
        print("   full curve (E: model/meas):", " ".join(
            f"{E}:{mf_model(E,*th):.3f}/{(data[E][1]/data[E][0]):.3f}" for E in sorted(data) if E > 1))

if __name__ == "__main__":
    main()
