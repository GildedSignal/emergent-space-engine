#!/usr/bin/env python3
"""Fermi ledger for 10^9 bodies on the 8 GB M1.

All repo-measured anchors are cited inline. Two parts:
  A. probe-B MC: element-change distribution of one encounter (flyby impulse at b < rho),
     entropy of the quantized delta, sub-quantum crossing rates per mass class.
  B. the budget table: static memory, H_live growth, throughput, bandwidth, per layout.
Output: everything printed; regenerable in ~20 s.
"""
import math, random

random.seed(20261008)

# ---- repo anchors (cited) -------------------------------------------------------
KICK_US = 29.0          # us per kick, plane measured (H0210 "kicks cost 29 us")
KICKS_PER_ORBIT = 32.5  # H0190 K1 (LEO, Moon/Sun tides)
AVG_FACTOR = 114.0      # H0190 K2 (first-order averaging)
PROG_BITS = 0.126       # bits/body, gold components-98bc (smooth belt program)
NAIVE_BITS = 157.0      # bits/body, naive quantized state
TUBE_B = 16.0           # law.md tube
WORK_PER_ENC = 786.0    # r8 v2 element-sort work per encounter
OPS = 1e10              # M1 simple ops/s across cores (board)
BW = 60e9               # B/s
RAM_BITS = 8e9 * 8
# probe A (this run, fixed sigma_e=1e-2, rho=1e-4, a in [1,1.5], 20 orbits):
PROBE_A = [(1000, 32), (2000, 169), (4000, 584)]
R8_BELT0 = 427 / 20.0   # encounters/orbit at N=1e4 (r8 v2, log-uniform draw)

# game scale: belt at 3 AU
AU = 1.496e11
A_M = 3 * AU
T_ORB = 2 * math.pi * math.sqrt(A_M**3 / (1.327e20))   # s, solar (2pi was missing)
V_K = 2 * math.pi * A_M / T_ORB          # m/s
T_LEO = 5400.0

# ---- probe A fit ----------------------------------------------------------------
import statistics
xs = [math.log(n) for n, _ in PROBE_A]
ys = [math.log(c / n / 20.0) for n, c in PROBE_A]
mx, my = statistics.mean(xs), statistics.mean(ys)
alpha = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
gamma0 = math.exp(my - alpha * mx)
pair_ratio = 970769 / 60720
print(f"[A] candidate pairs: x{pair_ratio:.2f} over x4 N -> exponent {math.log(pair_ratio)/math.log(4):.2f}")

# fluid cap: max conjunction rate per body per orbit in a 2D sheet (n * v_rel * 2rho swept)
def gamma_cap(N, width_a=0.5, v_rel=1e-2, rho=1e-4):
    n2d = N / (math.pi * (1.5**2 - 1.0))     # per area unit (a=1)
    return n2d * v_rel * 2 * rho * 2 * math.pi

# ---- probe B: one encounter's element change ------------------------------------
# 2D hyperbolic flyby at b < rho, relative speed v_rel ~ e-scale of the belt.
# delta_v = 2 G m / (b v_rel); |da|/a ~ 2 delta_v/v_K ; |de| ~ delta_v/v_K.
M_SUN = 1.989e30
MASSES = {"ship 1e6 kg": 1e6, "rock 1e12 kg": 1e12, "Ceres 9.4e20 kg": 9.4e20}
RHO_AU = 1e-4
NS = 200000
bs = [math.sqrt(random.random()) * RHO_AU for _ in range(NS)]        # flux ~ b db
vs = [abs(random.gauss(0, 1e-2)) + 1e-4 for _ in range(NS)]          # e-scale rel. speed (dimensionless)
print("\n[B] per-encounter element change |da|/a and quantum sensitivity")
print(f"{'mass':>18} {'median |da|/a':>14} {'eps where 50% cross':>20}")
mass_delta = {}
for name, m in MASSES.items():
    mu = m / M_SUN
    ds = sorted(2 * 2 * mu / (b * v) for b, v in zip(bs, vs))  # |da|/a = 2 dv/v_K, dv dim-less
    med = ds[NS // 2]
    mass_delta[name] = med
    eps50 = ds[NS // 4]  # quantum at which ~25% of single encounters already cross
    print(f"{name:>18} {med:14.2e} {eps50:20.2e}")

# ---- ledger ---------------------------------------------------------------------
print("\n[ledger] 10^9 bodies, T_orb(belt) = {:.1e} s, T_LEO = {:.0e} s".format(T_ORB, T_LEO))

def layout(name, N, gamma_pb_orbit, T, encounters=True):
    tot_enc_s = N * gamma_pb_orbit / T
    work_s = tot_enc_s * WORK_PER_ENC
    print(f"\n--- {name}")
    static_MB = N * PROG_BITS / 8 / 1e6
    print(f" static program store: {static_MB:.1f} MB (naive tubes {N*TUBE_B/1e9:.1f} GB > 8 GB -> programs mandatory)")
    print(f" encounters: {tot_enc_s:.3e}/s total; element-sort work {work_s:.3e} events/s"
          f" -> {work_s*1e-6:.1f} cores at 1 us/event, {work_s*KICK_US*1e-6:.0f} at today's 29 us")
    for mass_name, med in mass_delta.items():
        for eps_name, eps in [("2^-10", 2**-10), ("2^-20", 2**-20), ("2^-30", 2**-30)]:
            # sub-quantum accumulation: 1D walk, step ~ 2*med (sign random), crossing time (eps/step)^2 encounters
            step = 2 * med
            cross_frac = min(1.0, (step / eps) ** 2)
            dist_s = tot_enc_s * cross_frac * 40.0  # bits/s, ~40 bits per recorded scar
            tfill = RAM_BITS / dist_s if dist_s > 0 else float("inf")
            h = f"{tfill:.1e} s"
            print(f"   H_live[{mass_name}, eps={eps_name}]: {dist_s:.2e} bit/s -> 8GB in {h}")

# layout 1: all 10^9 in ONE 0.5-AU belt (local density extreme)
g_cap = gamma_cap(1e9)
g_pow = gamma0 * 1e9**alpha
g1 = min(g_cap, g_pow)
print(f" (dense-belt gamma: power-law {g_pow:.2e}/orbit, fluid cap {g_cap:.2e}; using {g1:.2e})")
layout("1) one dense belt, 1e9 bodies", 1e9, g1, T_ORB)
# layout 2: hierarchical, 1e5 sparse belts of 1e4 (r8-local density: per-body 2.1e-3/orbit)
layout("2) hierarchical, 1e5 x 1e4 belts (r8 belt-0 local rate)", 1e9, R8_BELT0 / 1e4, T_ORB)
# layout 3: LEO fleets
kicks_s = 1e9 * KICKS_PER_ORBIT / T_LEO
print(f"\n--- 3) all-LEO fleets")
print(f" kicks: {kicks_s:.2e}/s x {KICK_US} us = {kicks_s*KICK_US*1e-6:.0f} cores (board claims ~190)")
print(f" with 114x averaging: {kicks_s/AVG_FACTOR*KICK_US*1e-6:.1f} cores")
print(f" kicks at 0.3 us needed for 1.8 cores: {kicks_s*0.3e-6:.2f} cores")
print(f" bandwidth (24 B random per kick-event): {kicks_s*24/1e9:.3f} GB/s vs 60")
