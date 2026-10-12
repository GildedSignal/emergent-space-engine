#!/usr/bin/env python3
"""Probe: does range-scaling (Hurst-type) H separate bounded from compounding error
where B12's current global growth exponent misranks?

Statistic per seed:
  H  = slope of log R(k) vs log k over the TOP 3 dyadic octaves (k = N/8, N/4, N/2),
       R(k) = median over the N/k disjoint windows of (max - min).
  gE = current B12-style exponent: slope of log(|e|_max-to-date) vs log t over t >= 1
       (all series sit above the 1e-12 floor by construction; amplitudes ~1e-6).
Rule (frozen from calibration midpoints): H <= 0.33 -> bounded; else compounding.
Gate verdict = median H over seeds (board rule: median seed), and median gE (current gate).

All series length N = 2**14, 64 seeds, seeded deterministically (PCG64, seed = hash).
"""
import json
import numpy as np

N = 1 << 14
SEEDS = 64
FLOOR = 1e-12

rng_master = np.random.default_rng(20261012)


def series(seed, kind):
    r = np.random.default_rng(seed)
    t = np.arange(N, dtype=np.float64)
    A = 1e-6 * np.exp(r.uniform(np.log(0.3), np.log(3.0)))  # amplitude ~1e-6 (log-uniform)
    w = r.uniform(0.01, 0.2)  # oscillation frequency
    ph = r.uniform(0, 2 * np.pi)
    noise = r.normal(0, 0.02 * A, N)
    if kind == "bounded_band":            # rises to a band, then oscillates (a good law)
        ramp = 1 - np.exp(-t / (N / 64.0))
        return A * ramp * np.sin(w * t + ph) + noise
    if kind == "bounded_osc_noise":       # band + AR(1) microstructure + noise
        ar = np.empty(N)
        x = 0.0
        for i in range(N):
            x = 0.9 * x + r.normal(0, 0.1 * A)
            ar[i] = x
        return A * np.sin(w * t + ph) + ar + noise
    if kind == "diffusive_leak":          # slow random walk (the bad slow leak)
        step = 1e-4 * A
        return np.cumsum(r.normal(0, step, N))
    if kind == "linear_leak":             # systematic bias + noise (broke the recurrence ratio)
        return 2e-5 * A * t + noise
    if kind == "explosive":
        lam = 3.0 / N
        return A * np.exp(lam * t) * (1 + 0.02 * np.random.default_rng(seed + 1).normal(0, 1, N) * 0)
    # held-out
    if kind == "near_unit_root":
        x = np.empty(N)
        v = 0.0
        for i in range(N):
            v = 0.995 * v + r.normal(0, 0.05 * A)
            x[i] = v
        return x + noise
    if kind == "reflected_rw":
        step = 0.02 * A
        B = 10 * step * np.sqrt(N) / np.sqrt(N) * 10  # walls at +-10 sigma_step*sqrt-scale
        B = 10 * step * np.sqrt(64.0)
        x = np.empty(N)
        v = 0.0
        for i in range(N):
            v = v + r.normal(0, step)
            if v > B:
                v = B - (v - B)  # reflect
            elif v < -B:
                v = -B - (v + B)
            x[i] = v
        return x
    if kind == "bounded_plus_jumps":      # band + rare jumps, mean-reverting (re-anchoring law)
        e = A * np.sin(w * t + ph) + noise
        n_j = 5
        for j in range(n_j):
            i0 = r.integers(0, N - 1)
            e[i0] += 3 * A
            # mean-revert the offset with tau = N/32
            tau = N / 32.0
            off = 3 * A * np.exp(-np.arange(N - i0) / tau)
            e[i0:] += off - off[0] * 0  # offset appears at i0 and decays
        return e
    if kind == "sin_drift":               # bounded band + tiny systematic drift
        return A * np.sin(w * t + ph) + 2e-5 * A * t + noise
    raise ValueError(kind)


def H_hat(e):
    ks = [N // 8, N // 4, N // 2]
    logR, logk = [], []
    for k in ks:
        m = N // k
        w = e[: m * k].reshape(m, k)
        R = np.median(w.max(axis=1) - w.min(axis=1))
        if R <= 0:
            R = np.abs(e).max() + 1e-300
        logR.append(np.log(R))
        logk.append(np.log(k))
    return float(np.polyfit(logk, logR, 1)[0])


def growth_exponent(e):  # current B12 style: slope of log(max|e| so far) vs log t
    t = np.arange(1, len(e) + 1)
    mx = np.maximum.accumulate(np.abs(e)) + FLOOR
    # only where above the floor (all of it here, by construction)
    return float(np.polyfit(np.log(t), np.log(mx), 1)[0])


CAL = ["bounded_band", "bounded_osc_noise", "diffusive_leak", "linear_leak", "explosive"]
HELD = ["near_unit_root", "reflected_rw", "bounded_plus_jumps", "sin_drift"]

out = {"per_class": {}, "threshold": 0.33}
for kind in CAL + HELD:
    Hs, gEs = [], []
    for s in range(SEEDS):
        e = series(1_000_003 * s + 7919, kind)
        Hs.append(H_hat(e))
        gEs.append(growth_exponent(e))
    Hs, gEs = np.array(Hs), np.array(gEs)
    out["per_class"][kind] = {
        "held_out": kind in HELD,
        "H_median": float(np.median(Hs)),
        "H_q10_q90": [float(np.quantile(Hs, 0.1)), float(np.quantile(Hs, 0.9))],
        "verdict_H": "bounded" if np.median(Hs) <= out["threshold"] else "compounding",
        "gE_median": float(np.median(gEs)),
        "gE_q10_q90": [float(np.quantile(gEs, 0.1)), float(np.quantile(gEs, 0.9))],
        "verdict_current_B12": "pass" if np.median(gEs) <= 0.2 else "fail",
    }

# Prediction 5's noise-floor sensitivity on a bounded band: subsample at stride 7 vs stride 11
fl = []
for stride in (1, 7, 11):
    gEs = []
    for s in range(SEEDS):
        e = series(1_000_003 * s + 7919, "bounded_band") + np.random.default_rng(s).normal(0, 1e-12, N)
        gEs.append(growth_exponent(e[::stride]))
    fl.append(float(np.median(gEs)))
out["floor_sensitivity_gE_strides_1_7_11"] = fl

json.dump(out, open("probe_b12_metrics.json", "w"), indent=1)

hdr = f"{'class':<20}{'H med':>8}{'H q10-q90':>20}{'H verdict':>12}{'gE med':>9}{'gE verdict':>12}"
print(hdr)
print("-" * len(hdr))
for kind, d in out["per_class"].items():
    tag = "*" if d["held_out"] else " "
    q = d["H_q10_q90"]
    print(f"{tag+kind:<20}{d['H_median']:>8.3f}  [{q[0]:>5.2f},{q[1]:>5.2f}]"
          f"{d['verdict_H']:>12}{d['gE_median']:>9.3f}{d['verdict_current_B12']:>12}")
print(f"\nnoise-floor sensitivity, current gE on bounded_band at strides 1/7/11: "
      f"{fl[0]:.3f} / {fl[1]:.3f} / {fl[2]:.3f}  (gate threshold 0.2)")
