#!/usr/bin/env python3
"""Follow-up: cumulative first-scar saturation curves vs Gaussian-walk and
range-law references (same seeds, deterministic)."""
import json
import numpy as np
import hlive

N, ORBITS, Gm, eps, vdisp = 256, 40, 6e-7, 0.02, 0.04

out = {}
for seed in (1, 2):
    AD, _ = hlive.run(seed, N, ORBITS, Gm, eps, vdisp)
    d = np.diff(AD, axis=0)
    seedout = {}
    for dim, name in ((0, "A"), (1, "D")):
        sig = float(np.sqrt((d[:, :, dim] ** 2).mean()))
        curves = {}
        for qfac in (4, 8, 16, 32):
            Q = sig * qfac
            off = AD[:, :, dim] - AD[0, :, dim][None, :]
            sd = hlive.sigmadelta(off, Q)
            # cumulative distinct bodies scarred vs orbit
            first = sd["first"]
            cum = np.array([(first >= 0) & (first <= k + 1) for k in range(ORBITS)]).mean(axis=1)
            # references at k = 40 (Gaussian MC, same sigma, same orbit count)
            rng = np.random.default_rng(seed + 100)
            steps = rng.normal(0, sig, size=(ORBITS, N))
            walk = np.cumsum(steps, axis=0)
            crossed = (np.abs(walk) > Q / 2).any(axis=0).mean()
            # by-orbit cumulative for MC too
            cum_mc = (np.abs(walk) > Q / 2).cumsum(axis=0) > 0
            cum_mc = cum_mc.mean(axis=0)
            curves[f"qfac{qfac}"] = dict(
                Q=Q, measured_cum=cum.tolist(), gauss_mc_cum=cum_mc.tolist(),
                mc_end=float(crossed),
                measured_end=float(cum[-1]),
                k10_measured=float(cum[9]))
        seedout[name] = dict(sigma_per_orbit=sig, curves=curves)
    out[f"seed{seed}"] = seedout

with open("curves.json", "w") as f:
    json.dump(out, f, indent=1)
print("ok")
for seed in out:
    for name in ("A", "D"):
        for qf, c in out[seed][name]["curves"].items():
            print(seed, name, qf, "end: meas %.3f gauss %.3f | k10 meas %.3f" % (
                c["measured_end"], c["mc_end"], c["k10_measured"]))
