#!/usr/bin/env python3
"""Library-lens decisive experiments (run 20260930-1241).

A: law form — binary threshold-flip (minority-rule style, absorbing commitment)
   vs graded renegotiation (linear averaging + noise), matched activity at N=1e3.
   Measures what the geometry consumes (aggregate fraction): cross-population SD,
   sustained time-SD (surprise generation), flip-rate tail p99/p50, 1% forced noise.
B: aggregate exactness — Poisson dipole fluctuation ~ 1/sqrt(n); occupancy threshold
   n* = (1/eps_rel)^2 where individual identity is below the count's quantum.

FAST=1 gives a <60 s checker mode (N<=1e5, fewer pops/steps); default is the full run
(~8 min, includes N=1e6).
"""
import json
import os

import numpy as np

FAST = os.environ.get("FAST") == "1"
RNG = np.random.default_rng(20260930)
K = 4  # ring lattice neighbors (i+-1, i+-2)

def neighbors_mean(x):
    return (np.roll(x, 1) + np.roll(x, -1) + np.roll(x, 2) + np.roll(x, -2)) / K

# ---------------- law A1: binary threshold flip, rare reversion ----------------
def run_binary(N, steps, seed, delta, p_contact=0.5, force_noise=0.0, burn=300):
    rng = np.random.default_rng(seed)
    s = (rng.random(N) < 0.03).astype(np.float64)  # small seed minority
    frac_ts, flip_ts = [], []
    for t in range(steps + burn):
        u = neighbors_mean(s)
        infect = (s < 0.5) & (rng.random(N) < p_contact * (1.0 - (1.0 - u) ** K))
        revert = (s > 0.5) & (rng.random(N) < delta)
        if force_noise > 0:
            forced = rng.random(N) < force_noise
            s = np.where(forced, 1.0 - s, s)
        s = np.where(infect | revert, 1.0 - s, s)
        if t >= burn:
            frac_ts.append(s.mean())
            flip_ts.append((infect | revert).sum())
    return np.array(frac_ts), np.array(flip_ts)

# ---------------- law A2: graded renegotiation (linear + noise) ----------------
def run_graded(N, steps, seed, sigma, eps=0.5, force_noise=0.0, burn=300):
    rng = np.random.default_rng(seed)
    x = 0.30 + 0.05 * (rng.random(N) - 0.5)  # start near the same equilibrium
    frac_ts, ev_ts = [], []
    for t in range(steps + burn):
        u = neighbors_mean(x)
        dx = eps * (u - x) + sigma * (rng.random(N) - 0.5)
        x = np.clip(x + dx, 0.0, 1.0)
        if force_noise > 0:
            forced = rng.random(N) < force_noise
            x = np.where(forced, 1.0 - x, x)
        if t >= burn:
            frac_ts.append(x.mean())
            ev_ts.append(int((np.abs(dx) > 0.05).sum()))
    return np.array(frac_ts), np.array(ev_ts)

# ---- calibrate delta (binary) for mean fraction 0.30 and sigma (graded) for
# ---- matched activity, at N=1e3 only (held-out sizes never touch these) --------
def calibrate():
    def mean_frac(delta):
        f, _ = run_binary(1000, 1200, 7, delta)
        return f.mean()
    lo, hi = 0.001, 2.0
    for _ in range(18):
        mid = 0.5 * (lo + hi)
        if mean_frac(mid) > 0.30:
            lo = mid
        else:
            hi = mid
    delta = 0.5 * (lo + hi)
    _, rB = run_binary(1000, 1500, 7, delta)
    act_B = rB.mean() / 1000.0

    def activity(sigma):
        _, rG = run_graded(1000, 1500, 7, sigma)
        return rG.mean() / 1000.0
    lo, hi = 0.005, 1.5
    for _ in range(14):
        mid = 0.5 * (lo + hi)
        if activity(mid) < act_B:
            lo = mid
        else:
            hi = mid
    sigma = 0.5 * (lo + hi)
    return delta, sigma, act_B

delta, sigma, act = calibrate()
print(f"calibrated: delta={delta:.4f} sigma={sigma:.4f} matched_activity/agent/step={act:.4f}")

# ---------------- measurements ----------------
POPS = 4 if FAST else 10
SIZES = [(10**3, 800), (10**4, 800), (10**5, 600)] if FAST else \
        [(10**3, 3000), (10**4, 3000), (10**5, 2000), (10**6, 800)]
res = {"calibration": {"delta": delta, "sigma": sigma, "matched_activity": act}, "A": {}, "B": {}}
print(f"{'N':>8} {'law':>7} {'crossPopSD':>10} {'timeSD':>9} {'p99/p50':>8} {'meanFrac':>8}")
for N, steps in SIZES:
    for law, fn, par in [("binary", run_binary, delta), ("graded", run_graded, sigma)]:
        pops = int(POPS if N <= 10**5 or FAST else 6)
        F, R = [], []
        for i in range(pops):
            f, r = fn(N, steps, 100 + i, par)
            F.append(f)
            R.append(r)
        means = np.array([f.mean() for f in F])
        tsd = float(np.mean([f.std() for f in F]))
        ratios = []
        for r in R:
            med = np.median(r)
            if med > 0:
                ratios.append(np.percentile(r, 99) / med)
        rec = dict(crossPopSD=float(means.std(ddof=1)), timeSD=tsd,
                   tail=float(np.mean(ratios)) if ratios else None,
                   meanFrac=float(means.mean()), pops=pops, steps=steps)
        res["A"][f"{law}_{N}"] = rec
        print(f"{N:8d} {law:>7} {rec['crossPopSD']:10.2e} {rec['timeSD']:9.2e} "
              f"{(rec['tail'] or float('nan')):8.2f} {rec['meanFrac']:8.4f}")

# held-out stress: 1% forced flips at N=1e5 (vs same law noise-free above)
for law, fn, par in [("binary", run_binary, delta), ("graded", run_graded, sigma)]:
    F = []
    for i in range(4 if FAST else 8):
        f, _ = fn(10**5, 1500 if not FAST else 600, 500 + i, par, force_noise=0.01)
        F.append(f.mean())
    res["A"][f"{law}_stress"] = dict(crossPopSD=float(np.std(F, ddof=1)), timeSD=None)
    print(f"stress 1% @1e5 {law:>7} crossPopSD={res['A'][f'{law}_stress']['crossPopSD']:.3e}")

# ---------------- experiment B: 1/sqrt(n) and occupancy threshold ----------------
rng = np.random.default_rng(777)
rows = {}
for n in [10**2, 10**3, 10**4]:
    dips = []
    for _ in range(100 if FAST else 400):
        pts = rng.random((n, 2))
        m = pts.mean(axis=0) - 0.5
        dips.append(np.hypot(*m))
    d = np.std(dips)
    rows[n] = dict(sd_dipole=float(d), sd_x_sqrt_n=float(d * np.sqrt(n)))
    res["B"][str(n)] = rows[n]
    print(f"n={n:6d} SD(dipole)={d:.5f}  SD*sqrt(n)={d * np.sqrt(n):.5f}")
c = np.mean([v["sd_x_sqrt_n"] for v in rows.values()])
spread = max(abs(v["sd_x_sqrt_n"] - c) / c for v in rows.values())
eps_rel = 2.0 ** -8
res["B"]["sqrt_n_constancy_rel_dev"] = spread
res["B"]["n_star_2^-8"] = float((1.0 / eps_rel) ** 2)
print(f"1/sqrt(n) constancy: max rel dev {spread:.3%};  n*(eps=2^-8) = {res['B']['n_star_2^-8']:.3e}")

json.dump(res, open("metrics-fast.json" if FAST else "metrics.json", "w"), indent=1)
print("wrote", "metrics-fast.json" if FAST else "metrics.json")
