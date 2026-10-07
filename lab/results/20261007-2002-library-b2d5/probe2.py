#!/usr/bin/env python3
"""P4 fix: temporal-load concentration at matched a. The dispersion index in
probe.py was computed over ALL bodies, so radial shear (n = a^-1.5) dominated
it; it could not test burstiness. Here: same mixed population (90% belt +
10% fleet at a=1.5), compare per-body calendar load for belt bodies and fleet
bodies inside the SAME a-slice [1.495, 1.505]. Fleet/belt ratio >~ 10 means
co-orbital concentration multiplies the calendar load by orders of magnitude
(Extremistan leg of the redundancy lesson). Also: time-binned burst index for
one fleet body vs one belt body (variance/mean of conjunction counts per
0.01-orbit bin over 1 orbit, exact Kepler phases).
"""
import json
import numpy as np
from probe import belt, partners_per_body, rate_subsample

n = 100_000
r = np.random.default_rng(5)
a = np.concatenate([1.0 + r.random(int(0.9 * n)), 1.5 + r.normal(0, 1e-4, int(0.1 * n))])
e = np.concatenate([r.rayleigh(0.05, int(0.9 * n)), np.full(int(0.1 * n), 0.001)])

# matched-slice loads: recompute rates for all bodies in the slice exactly
lo, hi = 1.495, 1.505
sel = np.where((a > lo) & (a < hi))[0]
n_m = a ** -1.5
order = np.argsort(a)
a_s, e_s, n_s = a[order], e[order], n_m[order]
q_s, Q_s = a_s * (1 - e_s), a_s * (1 + e_s)
ecap = min(3 * e.max(), 0.6)
half = 2 * ecap * a / (1 - ecap)
load = np.empty(len(sel))
for k, i in enumerate(sel):
    qi, Qi = a[i] * (1 - e[i]), a[i] * (1 + e[i])
    w = np.arange(np.searchsorted(a_s, a[i] - half[i], "left"),
                  np.searchsorted(a_s, a[i] + half[i], "right"))
    keep = w[(Q_s[w] >= qi) & (q_s[w] <= Qi)]
    keep = keep[a_s[keep] != a[i]]
    load[k] = (np.abs(n_s[keep] - n_m[i]) / (0.5 * (n_s[keep] + n_m[i]))).sum()
fleet = load[e[sel] < 0.01]
beltm = load[e[sel] > 0.01]
out = {
    "slice_bodies_belt": int(len(beltm)),
    "slice_bodies_fleet": int(len(fleet)),
    "belt_load_mean": float(beltm.mean()),
    "fleet_load_mean": float(fleet.mean()) if len(fleet) else None,
    "fleet_over_belt": float(fleet.mean() / beltm.mean()) if len(fleet) else None,
}

# temporal burst index: one belt body and one fleet body, conjunction times
# over one orbit, binned at 0.01 orbit. Phases uniform (sufficient statistics
# for burstiness of a stationary point process given rates).
rr = np.random.default_rng(9)
def burst(i, bins=100):
    qi, Qi = a[i] * (1 - e[i]), a[i] * (1 + e[i])
    w = np.arange(np.searchsorted(a_s, a[i] - half[i], "left"),
                  np.searchsorted(a_s, a[i] + half[i], "right"))
    keep = w[(Q_s[w] >= qi) & (q_s[w] <= Qi)]
    keep = keep[a_s[keep] != a[i]]
    syn = np.abs(n_s[keep] - n_m[i]) / (0.5 * (n_s[keep] + n_m[i]))  # events/orbit
    times = []
    for s in syn:
        period = 1.0 / max(s, 1e-12)
        times.append(rr.random() + np.arange(0, 1, period))
    t = np.concatenate(times) if times else np.array([])
    h, _ = np.histogram(t % 1.0, bins=bins)
    return float(h.var() / h.mean()) if h.mean() > 0 else 0.0
ib = sel[np.argmax(e[sel] > 0.01)] if (e[sel] > 0.01).any() else sel[0]
if_ = sel[np.argmin(e[sel])] if len(fleet) else sel[0]
out["burst_belt_body"] = burst(int(ib))
out["burst_fleet_body"] = burst(int(if_))
out["burst_poisson_ref"] = 1.0

with open(__import__("pathlib").Path(__file__).parent / "probe2-out.json", "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1))
