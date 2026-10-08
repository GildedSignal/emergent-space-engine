#!/usr/bin/env python3
"""Decade-local growth exponents of running-max |dE/E0| on the frozen probe-1 code.

Verdicts on record (held out): fixed-dt = bounded (1.8e-8); mandated variable
step rule = walks then saturates (~8.65e-4). Synthetic cases calibrate alpha.
Run: python3 horizon_exponent.py   (each probe command < 60 s)
"""
import math, random, sys, os, json

EV = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
                  "artifacts/evidence/gravity-v1-freeze-20260929/probe-scripts")
sys.path.insert(0, os.path.abspath(EV))
from run_energy2 import run_energy  # frozen; (p, e, eta, order, korbits, fixed_dt) -> (k, me, samples, steps)


def decade_exponents(m, ks):
    """alpha per decade: local slope of log(running max) vs log(orbit count)."""
    out = {}
    for d in range(0, 5):
        lo, hi = 10 ** d, 10 ** (d + 1)
        ilo = min(range(len(ks)), key=lambda i: abs(ks[i] - lo))
        ihi = min(range(len(ks)), key=lambda i: abs(ks[i] - hi))
        if ks[ihi] < hi * 0.5 or ihi <= ilo or m[ihi] <= 0 or m[ilo] <= 0:
            continue
        a = (math.log(m[ihi]) - math.log(m[ilo])) / (math.log(ks[ihi]) - math.log(ks[ilo]))
        out[d] = a
    return out


def window_slope(m, ks, k_lo, k_hi):
    """B12's current style: one slope over a window, ignoring decade structure."""
    ilo = min(range(len(ks)), key=lambda i: abs(ks[i] - k_lo))
    ihi = min(range(len(ks)), key=lambda i: abs(ks[i] - k_hi))
    return (math.log(m[ihi]) - math.log(m[ilo])) / (math.log(ks[ihi]) - math.log(ks[ilo]))


def report(name, samples):
    ks = [s[0] for s in samples]
    m = [s[1] for s in samples]
    de = decade_exponents(m, ks)
    line = " ".join(f"[{10**d}->{10**(d+1)}]:{v:+.2f}" for d, v in sorted(de.items()))
    print(f"{name:32s} {line}   max|dE|={max(m):.2e}")
    return de


def run(p, e, eta, order, K, fixed_dt=None):
    k, me, smp, st = run_energy(p, e, eta, order, K, fixed_dt=fixed_dt)
    return smp


res = {}
print("== frozen probe-1 data (regenerated with frozen code) ==")
smp = run(20.0, 0.2, 1/32, 2, 10000)  # variable rule (recorded verdict: walks)
res["variable_e02"] = report("variable-dt eta=1/32 o2 e=0.2", smp)
rref = (20.0/(1+0.2) * 20.0/(1-0.2)) ** 0.5
smp = run(20.0, 0.2, 1/32, 2, 10000, fixed_dt=1/32 * rref**1.5)  # frozen fixed-dt convention
res["fixed_e02"] = report("fixed-dt    eta~1/32 o2 e=0.2", smp)
smp = run(20.0, 0.5, 1/32, 2, 10000)  # held-out eccentricity
res["variable_e05"] = report("variable-dt eta=1/32 o2 e=0.5", smp)
rref5 = (20.0/(1+0.5) * 20.0/(1-0.5)) ** 0.5
smp = run(20.0, 0.5, 1/32, 2, 10000, fixed_dt=1/32 * rref5**1.5)
res["fixed_e05"] = report("fixed-dt    eta~1/32 o2 e=0.5", smp)

print("== synthetic calibrations ==")
random.seed(7)
N = 100000
x, m = 0.0, []
for k in range(1, N + 1):
    x += random.gauss(0, 1)
    m.append(max(m[-1] if m else 0.0, abs(x)))
ms = [(k + 1, v) for k, v in enumerate(m)]
res["random_walk"] = report("random walk (control)", ms)

m = []
for k in range(1, N + 1):
    v = 1e-8 * (1 + 0.5 * math.sin(k / 30.0))
    m.append(max(m[-1] if m else 0.0, v))
ms = [(k + 1, v) for k, v in enumerate(m)]
res["bounded"] = report("bounded oscillation (control)", ms)

m = []
for k in range(1, N + 1):
    v = 8.65e-4 * (1 - math.exp(-k / 50.0)) * (1 + 0.5 * math.sin(k / 30.0))
    m.append(max(m[-1] if m else 0.0, v))
ms = [(k + 1, v) for k, v in enumerate(m)]
res["transient"] = report("bounded w/ transient (adversarial)", ms)
w = window_slope([v for _, v in ms], [k for k, _ in ms], 1, 1000)
res["transient_window_slope_1_1000"] = w
print(f"   single-window slope [1->10^3] (B12 style): {w:+.2f}  (>0.2 would misclassify as compounding)")

json.dump(res, open("exponents.json", "w"), indent=1)
print("wrote exponents.json")
