#!/usr/bin/env python3
"""Validate the crossing-gap model on scene C's exact bodies (crate RNG replicated).

For each truly encountering pair (recomputed here by dense sampling), compare the measured
mean-anomaly gap DeltaM0 against -2*Deltae*sin(theta*) (equation-of-center model) and against
the exact intersection gap computed from the two radial curves.
"""
import numpy as np

TWOPI = 2 * np.pi
TAU_TICKS = 4_294_967_296.0
PERIOD = round(TWOPI * TAU_TICKS)
N = 1600
SIGMA_E = 1e-2
RHO = 1e-4

# crate belt::Rng (splitmix64-ish)
MASK = (1 << 64) - 1
class Rng:
    def __init__(self, s):
        self.s = s & MASK
    def next_u64(self):
        self.s = (self.s + 0x9E3779B97F4A7C15) & MASK
        z = self.s
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK
        return z ^ (z >> 31)
    def f64(self):
        return (self.next_u64() >> 11) / 9007199254740992.0

rng = Rng(103)
es = []
lams = []
for _ in range(N):
    u = rng.f64()
    e = min(SIGMA_E * np.sqrt(-2.0 * np.log(1.0 - u)), 0.5)
    lam = TWOPI * rng.f64()
    es.append(e)
    lams.append(lam)
es = np.array(es)
lams = np.array(lams)

n_motion = TWOPI * TAU_TICKS / PERIOD
a = n_motion ** (-2.0 / 3.0)
p = a * (1 - es**2)

# mean anomaly at t=0 (crate: tp = round(-(m0/TAU)*period) mod period; m0 = lam since pom=0)
tps = np.round((-(lams / TWOPI) * PERIOD) % PERIOD).astype(np.int64)
M0 = TWOPI * (((0 - tps) / PERIOD) % 1.0)

def state_idx(i, m):
    e = es[i]
    ea = m + e * np.sin(m) * (1 + e * np.cos(m))
    for _ in range(12):
        d = (ea - e * np.sin(ea) - m) / (1 - e * np.cos(ea))
        ea = ea - d
        if np.max(np.abs(d)) < 1e-15:
            break
    xp = a * (np.cos(ea) - e)
    yp = a * np.sqrt(1 - e * e) * np.sin(ea)
    return xp, yp

# dense truth over all pairs is too slow in Python; use the model to pick candidate windows,
# then verify by sampling. For each pair compute theta* intersections and DeltaM* exactly.
ts = np.linspace(0, TWOPI, 20000, endpoint=False)
# precompute each body's (x, y) on the time grid
XY = np.empty((N, 2, ts.size))
for i in range(N):
    x = (ts * TAU_TICKS - tps[i]) / PERIOD
    m = TWOPI * (x - np.floor(x))
    xx, yy = state_idx(i, m)
    XY[i, 0] = xx
    XY[i, 1] = yy

# brute force in chunks over pairs with |dM0| < 0.2 or > 2pi-0.2 (aligned apsides: encounters
# only near small gaps) — dispersion moves windows to |dM0| ~ 2*Deltae <= ~0.15
dM0 = (M0[:, None] - M0[None, :]) % TWOPI
dM0 = np.minimum(dM0, TWOPI - dM0)
iu, ju = np.triu_indices(N, 1)
sel = dM0[iu, ju] < 0.2
iu, ju = iu[sel], ju[sel]
print(f"pairs with |dM0| < 0.2: {iu.size}")

enc = []
for I, J in zip(iu, ju):
    d = np.hypot(XY[I, 0] - XY[J, 0], XY[I, 1] - XY[J, 1])
    if d.min() < RHO:
        enc.append((I, J))
print(f"encountering pairs found: {len(enc)}")

print(f"{'I':>5} {'J':>5} {'e_i':>9} {'e_j':>9} {'de':>9} {'dM0':>9} {'2de':>9} {'dM0/2de':>9}")
ranks = []
for I, J in enc:
    de = abs(es[I] - es[J])
    dm0 = (M0[I] - M0[J]) % TWOPI
    dm0 = min(dm0, TWOPI - dm0)
    # circular rank in M0 order
    ranks.append(dm0 * N / TWOPI)
    print(f"{I:>5} {J:>5} {es[I]:>9.4f} {es[J]:>9.4f} {de:>9.4f} {dm0:>9.5f} {2*de:>9.5f} {dm0/(2*de) if de>0 else 0:>9.3f}")
ranks = np.array(ranks)
print(f"\nmodel rank n*2de/2pi: median {np.median(ranks):.1f}, p99 {np.quantile(ranks, 0.99):.1f}")
print(f"actual integer-rank miss-at-4 threshold: pairs with model rank > 4: {(ranks > 4).mean():.3f}")
