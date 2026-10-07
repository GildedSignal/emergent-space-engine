#!/usr/bin/env python3
"""Run 20261007-0711-library-9ab7 — the tail probe (predictions.md).

Three per-frame work streams share p50/p95/p99.9 as seen by a 10-min bench
(36k frames at 60 Hz) but differ in tail exponent. Compare: the true
once-per-hour frame (analytic) against three budget-sizing rules (bench max,
Gaussian moments, Hill-exponent extrapolation). Then a preemptive queue sim
with budget B and backlog carryover (the plane's overflow = RTF dip) measures
hitch rate vs utilization and FIFO vs EDF. Structure-level probe: synthetic
streams shaped like the engine's work generators, not engine timings.
"""
import json
import numpy as np
from statistics import NormalDist

rng = np.random.default_rng(20261007)
BENCH = 36_000
P_HITCH = 4.6e-6
Z = NormalDist().inv_cdf(1 - P_HITCH)
BASE = 4.0
Q_BURST = 0.005
MATCH = {}

def draw_bursts(kind, alpha, k):
    if kind == "light":
        return rng.lognormal(np.log(6.0), 0.45, k)
    sc = MATCH.get(kind, 1.0)
    return sc * (1.0 - rng.random(k)) ** (-1.0 / alpha)

def stream(kind, alpha, n):
    w = BASE + rng.poisson(0.3, n) * 0.2
    hit = rng.random(n) < Q_BURST
    w[hit] += draw_bursts(kind, alpha, int(hit.sum()))
    return w

KINDS = [("light", None), ("par30", 3.0), ("par15", 1.5)]

# pass 1: fix Pareto scales so the bench p99.9 matches the light stream's
light = stream("light", None, BENCH)
ref = float(np.quantile(light, 0.999))
for kind, alpha in KINDS[1:]:
    p0 = float(np.quantile(stream(kind, alpha, BENCH), 0.999))
    MATCH[kind] = (ref - BASE) / (p0 - BASE)

rep = {"benches": {}, "sizing": {}, "queue": {}, "order": {}, "budget_rule": ref}
print(f"budget sized by bench p99.9 = {ref:.2f} (all streams)")
print(f"{'stream':8s} {'p50':>6s} {'p95':>6s} {'p99.9':>6s} | "
      f"{'truth/h':>8s} {'benchMax':>8s} {'gauss':>8s} {'hill':>8s}")

for kind, alpha in KINDS:
    p999s, hills, gausses, maxes = [], [], [], []
    for _ in range(10):
        s = stream(kind, alpha, BENCH)
        p999s.append(np.quantile(s, 0.999))
        maxes.append(s.max())
        mu, sd = s.mean(), s.std(ddof=1)
        gausses.append(mu + Z * sd)
        x = np.sort(s)
        k = 360
        ahat = k / np.sum(np.log(x[-k:] / x[-k - 1]))
        u = np.quantile(s, 0.99)
        hills.append(u * (0.01 / P_HITCH) ** (1.0 / ahat))
    lv = P_HITCH / Q_BURST
    if kind == "light":
        z = NormalDist().inv_cdf(1 - lv)
        truth = BASE + float(np.exp(np.log(6.0) + 0.45 * z))
    else:
        truth = BASE + MATCH[kind] * lv ** (-1.0 / alpha)
    show = stream(kind, alpha, BENCH)
    rep["benches"][kind] = dict(p50=float(np.quantile(show, .5)),
                                p95=float(np.quantile(show, .95)),
                                p999=float(np.quantile(show, .999)))
    rep["sizing"][kind] = dict(truth=truth, bench_max=float(np.mean(maxes)),
                               gauss=float(np.mean(gausses)),
                               hill=float(np.mean(hills)),
                               hill_sd=float(np.std(hills)))
    r = rep["sizing"][kind]
    print(f"{kind:8s} {rep['benches'][kind]['p50']:6.2f} "
          f"{rep['benches'][kind]['p95']:6.2f} {rep['benches'][kind]['p999']:6.2f} | "
          f"{truth:8.1f} {r['bench_max']:8.1f} {r['gauss']:8.1f} "
          f"{r['hill']:8.1f} (sd {r['hill_sd']/r['hill']:.0%})")

# --- queue sim ---------------------------------------------------------------
def mean_load(kind, alpha):
    return float(stream(kind, alpha, 200_000).mean())

def run_queue(kind, alpha, rho, order, n=200_000):
    B = mean_load(kind, alpha) / rho
    pending = []                       # [deadline_frame, remaining_work]
    hitches = misses = 0
    for f in range(n):
        pending.append([f + 3, 1.0])
        if rng.random() < Q_BURST:
            nsplit = int(rng.integers(2, 6))
            d = f + int(rng.integers(1, 4))
            b = float(draw_bursts(kind, alpha, 1)[0])
            for _ in range(nsplit):
                pending.append([d, b / nsplit])
        if order == "edf":
            pending.sort(key=lambda j: j[0])
        budget = B
        rest = []
        for i, j in enumerate(pending):
            if budget <= 1e-12:
                rest.extend(pending[i:])
                break
            use = min(budget, j[1])
            j[1] -= use
            budget -= use
            if j[1] <= 1e-12:
                if f > j[0]:
                    misses += 1
            else:
                rest.append(j)
        pending = rest
        if sum(j[1] for j in pending) > B:
            hitches += 1
    return hitches / n, misses / n

print("\nhitch = leftover work at frame end > one full budget (RTF<=50% next frame)")
for kind, alpha in [("light", None), ("par15", 1.5)]:
    row = {}
    for rho in (0.5, 0.7, 0.9):
        h, m = run_queue(kind, alpha, rho, "fifo")
        row[str(rho)] = [h, m]
        print(f"  {kind:6s} rho={rho:.1f}  hitch/frame={h:.2e} "
              f"(per hour={h*216000:.2f})  miss/frame={m:.2e}")
    rep["queue"][kind] = row

print("\nFIFO vs EDF at rho=0.7")
for kind, alpha in [("light", None), ("par15", 1.5)]:
    hf, mf = run_queue(kind, alpha, 0.7, "fifo")
    he, me = run_queue(kind, alpha, 0.7, "edf")
    rep["order"][kind] = dict(fifo=[hf, mf], edf=[he, me])
    print(f"  {kind:6s} hitch fifo={hf:.2e} edf={he:.2e} "
          f"({abs(hf-he)/max(hf,1e-300):.1%}); miss fifo={mf:.2e} edf={me:.2e} "
          f"({abs(mf-me)/max(mf,1e-300):.1%})")

json.dump(rep, open("probe_out.json", "w"), indent=1)
print("\nwrote probe_out.json")
