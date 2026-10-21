#!/usr/bin/env python3
"""Window-scale mixing time: evolve the g=25 census with constant steps (no drift -> conservative)
for 120 fires and watch max/μ decay toward the Poisson floor. usage: evolve.py <census> <log> <g0>"""
import re
import sys

import numpy as np

census, log, g0 = sys.argv[1], sys.argv[2], int(sys.argv[3])
step_med, tgs = None, {}
for line in open(log):
    m = re.search(r"step_med=([\d.e+]+)", line)
    if m and step_med is None:
        step_med = float(m.group(1))
    m = re.match(r"gen g=(\d+) t=(-?\d+)", line)
    if m:
        tgs[int(m.group(1))] = int(m.group(2))
rows = np.loadtxt(census)
sel = rows[rows[:, 0] == g0]
sel = sel[np.argsort(sel[:, 1])]
due, step = sel[:, 2].copy(), sel[:, 3].copy()
N, W = len(due), int(step_med / 64)
rng = np.random.default_rng(3)
floor_max = np.median([np.sort(np.bincount(rng.integers(0, 64, N), minlength=64))[-1] * 64 / N for _ in range(2000)])
t0 = tgs[g0]
print(f"N={N} g0={g0} floor={floor_max:.3f}")
for j in list(range(1, 41, 4)) + list(range(40, 121, 10)):
    t = t0 + int(j * 1.03 * step_med * (64 / 64))  # same census spacing as the flight
    k = (t - due) // step + 1
    d = due + k * step
    lo, hi = t, t + int(step_med)
    kk = ((d - lo) // W).astype(np.int64)
    nwin = max(int((hi - lo) / W), 1)
    c = np.bincount(kk[(kk >= 0) & (kk < nwin)], minlength=nwin)[:nwin]
    mu = N / nwin
    print(f"fire {j:3d} max/mu {c.max() / mu:.3f} p99/mu {np.sort(c)[int(0.99 * (len(c) - 1))] / mu:.3f}")
