#!/usr/bin/env python3
"""Debug: does a kicked body (e = de, aligned apsides) really encounter its circular formation?

Dense direct sampling of d(t) over one period for the partners whose mean-anomaly gap is
closest to the predicted crossing gap -2*de (equation of center). No window/conjunction logic.
"""
import numpy as np

TWOPI = 2 * np.pi
T = TWOPI  # a = 1, n = 1
TAU_TICKS = 4_294_967_296.0
PERIOD_TICKS = round(TWOPI * TAU_TICKS)
N = 1600
DE = 1e-2
RHO = 1e-4

rng = np.random.default_rng(0)  # not the crate's rng; only used to pick lam offsets for debug
lam = rng.uniform(0, TWOPI, N - 1)  # the circular partners (values here only illustrative)

# body states, exact crate convention: with_period(period, e, pom=0, lam0)
# a = n^(-2/3) with n = TAU*TICKS/period -> a ~ 1; M(t) = TAU*frac((t*TICKS - tp)/period)
# tp = round(-(m0/TAU)*period) mod period, m0 = lam0 - pom

def state(a, e, m0, t):
    # mean anomaly at t (crate formula)
    per = PERIOD_TICKS
    tp = round((-(m0 / TWOPI) * per) % per)
    x = (t * TAU_TICKS - tp) / per
    m = TWOPI * (x - np.floor(x))
    # Newton on Kepler
    ea = m + e * np.sin(m) * (1 + e * np.cos(m))
    for _ in range(12):
        d = (ea - e * np.sin(ea) - m) / (1 - e * np.cos(ea))
        ea = ea - d
        if np.max(np.abs(d)) < 1e-15:
            break
    xp = a * (np.cos(ea) - e)
    yp = a * np.sqrt(1 - e * e) * np.sin(ea)
    return xp, yp  # pom = 0

n_motion = TWOPI * TAU_TICKS / PERIOD_TICKS
a_eff = n_motion ** (-2.0 / 3.0)
print(f"a_eff = {a_eff!r}")

# kicked body 0: e = DE, lam0 = 0.3 (arbitrary)
lam0 = 0.3
# partners circular
m0_partners = lam  # pom = 0

# predicted crossing: cos(nu*) = -(e_i + e_j)/(1 + e_i e_j) ~ -DE
nu_star = np.arccos(-DE / (1 + 0))  # ~ pi/2 + DE
M0_star = nu_star - 2 * DE * np.sin(nu_star)   # kicked body's mean anomaly at crossing
Mj_star = nu_star                                # circular partner
dM_star = M0_star - Mj_star
print(f"nu* = {nu_star}, dM* = {dM_star} (predicted -2*DE = {-2*DE})")

# mean anomaly of body 0 at t=0
tp0 = round((-(lam0 / TWOPI) * PERIOD_TICKS) % PERIOD_TICKS)
M0_0 = TWOPI * (((0 * TAU_TICKS - tp0) / PERIOD_TICKS) % 1.0)
# partners' M at t=0
dM0 = (M0_0 - m0_partners) % TWOPI  # locked gap

# closest partners to both crossing windows
for target in [dM_star % TWOPI, (-dM_star) % TWOPI]:
    dist = np.abs((dM0 - target + np.pi) % TWOPI - np.pi)
    idx = np.argsort(dist)[:8]
    print(f"target dM* = {target:.5f}: best gaps {dist[idx]}")

# dense-sample the best 40 partners overall
targets = np.array([dM_star % TWOPI, (-dM_star) % TWOPI])
dist = np.min(np.abs(((dM0[:, None] - targets[None, :]) + np.pi) % TWOPI - np.pi), axis=1)
idx = np.argsort(dist)[:40]
ts = np.linspace(0, T, 400000)
x0, y0 = state(a_eff, DE, lam0, ts)
best = []
for j in idx:
    xj, yj = state(a_eff, 0.0, lam[j], ts)
    d = np.hypot(x0 - xj, y0 - yj)
    best.append((d.min(), j, dist[j]))
best.sort()
print("min distances (best 8 of 40 sampled):")
for dmin, j, g in best[:8]:
    print(f"  j={j} gap={g:.5f} dmin={dmin:.3e} {'ENC' if dmin < RHO else ''}")
