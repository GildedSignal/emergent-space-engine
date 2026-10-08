#!/usr/bin/env python3
"""H_live Fermi budget at 1e9 bodies on the 8 GB M1.

Part A: analytic decomposition (stock, creation rate, ceiling, 190-core cross-check).
Part B: Monte Carlo falsifier of the three load-bearing numbers (P1, P2, P3).
Units: SI throughout unless noted. 2D coplanar belt, shear-dominated encounters.
"""
import math
import numpy as np

AU = 1.495978707e11
G = 6.674e-11
MSUN = 1.9885e30
YEAR = 3.156e7

# ---------------- belt model (anchored on B18b: banded p, Rayleigh e, uniform angles)
# solar-asteroid-belt-like annulus scaled to N members; two body-mass cases.
A_IN, A_OUT = 1.8 * AU, 3.4 * AU
AREA = math.pi * (A_OUT**2 - A_IN**2)
A_MID = 0.5 * (A_IN + A_OUT)
OMEGA = math.sqrt(G * MSUN / A_MID**3)          # s^-1 at mid belt
PERIOD = 2 * math.pi / OMEGA
V_ORB = OMEGA * A_MID

N = 1e9
def belt(m_body):
    n = N / AREA                                 # surface number density m^-2
    r_hill = A_MID * (m_body / (3 * MSUN)) ** (1 / 3)
    return n, r_hill

def gamma_resolvable(n, m, q):
    """Rate per body of encounters with impulse > q (shear-dominated 2D)."""
    return 4 * n * G * m / q

print("=" * 72)
print("PART A — analytic budget, N = 1e9, belt 1.8-3.4 AU, area %.2e m^2" % AREA)
print("orbital period at mid-belt: %.2e s = %.2f yr" % (PERIOD, PERIOD / YEAR))

# --- stock terms
TOTAL_BITS = 4.5e9 * 8                           # 4.5 GB of the 8 GB for shipmem
bits_per_body_budget = TOTAL_BITS / N
prog_bits = 0.126 * N / 8                        # gold components-98bc
print("\n[stock] budget 4.5 GB -> %.0f bits/body; smooth program 0.126 b/b -> %.0f MB"
      % (bits_per_body_budget, prog_bits / 1e6))
for w in (8, 16, 24, 36):
    print("        catalogue at width %2d b/b -> %.2f GB (%.0f%% of budget)"
          % (w, w * N / 8 / 1e9, 100 * w / bits_per_body_budget))

# --- creation rate + write bandwidth, asteroid-like vs ship-like
print("\n[rate]  Gamma(Dv>q) = 4 n G m / q   (Omega cancels)")
for label, m in (("asteroid 100 m (1e13 kg)", 1.05e13), ("ship 1 kt (1e6 kg)", 1e6)):
    n, rh = belt(m)
    print("  %s: n = %.2e m^-2, r_H = %.2e m" % (label, n, rh))
    for q_rel in (1e-4, 1e-6, 1e-8):
        q = q_rel * V_ORB                        # quantum as fraction of orbital speed
        g = gamma_resolvable(n, m, q)
        print("    q = v_orb x %.0e : Gamma = %.2e /body/s = %.2e /body/orbit"
              % (q_rel, g, g * PERIOD))

# --- compute cross-check: the board's "190 cores at today's rates"
print("\n[compute] kick load at 32 kicks/orbit (H0190), ~60 ns/kick measured-class")
v_kick_ns = 60
for rtf in (1e2, 1e4, 1e6):
    kicks_per_gamesec = N * 32 / (PERIOD / rtf)
    cores = kicks_per_gamesec * v_kick_ns * 1e-9 / 4   # 4 performance cores busy
    print("  rtf %.0e: %.2e kicks/game-s -> %.1f perf-core equivalents"
          % (rtf, kicks_per_gamesec, cores))
print("  legacy rates for comparison: 500 steps/orbit at 1 us -> %.0f cores at rtf 5e4"
      % (N * 500 * 1e-6 / (PERIOD / 5e4) / 4))

# ---------------- PART B: Monte Carlo falsifier ----------------
rng = np.random.default_rng(20261008)
NB = 40000                                      # ensemble of independent bodies
ORBITS = 3e4
T = ORBITS * PERIOD

m = 1.05e13                                     # asteroid-like case
n, r_hill = belt(m)
Q_REL = 1e-6                                    # track the smallest quantum
q = Q_REL * V_ORB
bstar = math.sqrt(4 * G * m / (3 * OMEGA * q))  # impact param giving impulse = q
lam_total = gamma_resolvable(n, m, q) * T
print("=" * 72)
print("PART B — Monte Carlo, %d bodies, %.0e orbits, b* = %.2e m (r_H = %.2e m)"
      % (NB, ORBITS, bstar, r_hill))
assert bstar > r_hill, "quantum so coarse nothing resolves; pick finer q"

dv = np.zeros((NB, 2))
sigma_t, t_t = [], []
# log-spaced checkpoints to fit S vs log2 t
checks = np.logspace(math.log10(PERIOD / 100), math.log10(T), 24)
next_c = 0
t = 0.0
DT = T / 60                                     # 60 coarse steps, thin enough
counts_res = 0
macro = 3 * n * OMEGA * r_hill**2 * T           # encounters inside r_H (macro events)
while t < T:
    dt = min(DT, T - t)
    lam = gamma_resolvable(n, m, q) * dt
    k = rng.poisson(lam, NB)
    counts_res += k.sum()
    tot = k.sum()
    if tot:
        u = rng.random(tot)
        b = np.sqrt(r_hill**2 + u * (bstar**2 - r_hill**2))
        imp = 2 * G * m / (b * 1.5 * OMEGA * b)     # |Dv| = 2Gm/(b v_rel)
        th = rng.random(tot) * 2 * math.pi
        dvx = np.bincount(np.repeat(np.arange(NB), k), weights=imp * np.cos(th),
                          minlength=NB)
        dvy = np.bincount(np.repeat(np.arange(NB), k), weights=imp * np.sin(th),
                          minlength=NB)
        dv[:, 0] += dvx
        dv[:, 1] += dvy
    t += dt
    if next_c < len(checks) and t >= checks[next_c]:
        sigma_t.append(dv.std(axis=0).mean())       # per-component std
        t_t.append(t)
        next_c += 1

sigma_t = np.array(sigma_t); t_t = np.array(t_t)
S = np.log2(sigma_t / q)
lt = np.log2(t_t / PERIOD)
mask = (sigma_t < 0.05 * V_ORB) & (t_t > 10 * PERIOD)  # pre-saturation window
slope, icept = np.polyfit(lt[mask], S[mask], 1)
print("P1  measured resolvable-encounter rate %.3e /body/orbit; analytic %.3e"
      % (counts_res / NB / ORBITS, gamma_resolvable(n, m, q) * PERIOD))
print("P2  S(t) = log2(sigma/q) slope vs log2(t/orbit): %.3f  (predicted 0.5)" % slope)
print("    S at 1 orbit %.1f b/b, at %.0e orbits %.1f b/b"
      % (S[0], ORBITS, S[-1]))
print("    macro (b<r_H) events: %.2e /body/orbit -> O(100) bits each" %
      (macro / ORBITS))

# ---------------- P3: ceiling = marginal entropy of the B18b belt at law quanta
print("\nP3  ceiling: quantized marginal entropy of (a, e, phi), program gone")
NS = 4_000_000
a_s = rng.uniform(A_IN, A_OUT, NS)
e_s = rng.rayleigh(0.1, NS)
p_s = rng.random(NS) * 2 * math.pi

def h1d(x, dx, lo, hi):
    """Discretized 1-D entropy with occupancy >> 1 per bin (plug-in safe)."""
    nb = max(8, int((hi - lo) / dx))
    cnt, _ = np.histogram(x, bins=nb, range=(lo, hi))
    pr = cnt[cnt > 0] / x.size
    return -(pr * np.log2(pr)).sum()

for da_rel, de, dphi in ((2**-10, 2**-8, 2**-16), (2**-12, 2**-10, 2**-16),
                         (2**-8, 2**-6, 2**-14)):
    da = da_rel * A_MID
    Ha = h1d(a_s, da, A_IN, A_OUT)
    He = h1d(e_s, de, 0.0, 0.6)
    Hp = h1d(p_s, dphi, 0.0, 2 * math.pi)
    H = Ha + He + Hp
    print("    quanta (da/a 2^-%d, de 2^-%d, dphi 2^-%d): H = %.1f bits/body"
          " (a %.1f + e %.1f + phi %.1f) -> %.2f GB at 1e9"
          % (-math.log2(da_rel), -math.log2(de), -math.log2(dphi),
             H, Ha, He, Hp, H * N / 8 / 1e9))

# write bandwidth: re-encode cost of above-quantum events, worst game pace
print("\n[write] events/game-s and catalogue write at rtf 1e6 (fastest pace shown):")
q6 = 1e-6 * V_ORB
for w_delta in (8, 32):
    ev = N * gamma_resolvable(n, m, q6) * 1e6          # events per game-second
    print("    q=1e-6 v, %2d-bit delta: %.2e events/game-s -> %.2f MB/s"
          % (w_delta, ev, ev * w_delta / 8 / 1e6))
