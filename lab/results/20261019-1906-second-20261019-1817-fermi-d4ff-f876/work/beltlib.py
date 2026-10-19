"""Shared library: shipped genesis port (verbatim from d4ff/checker-validated),
units, and the closed-form conjunction geometry.

Units: GM_sun = 1 (root^3 / root-time^2), c = 1 root/root-time.
1 root = 1.477 km, 1 root-time = 4.9268e-6 game-s.
Belt law: massless test bodies on exact planar Kepler orbits (no ship-ship
gravity wired; checker verified encounters enqueue no items).
"""
import math
import os
import numpy as np

MASK = (1 << 64) - 1
ROOT_KM = 1.477
C_KM_S = 299792.458
AU = 101_300_000                # root units (scenario.rs)
ROOT_T_S = ROOT_KM * 1e3 / (C_KM_S * 1e3)   # game-s per root-time
LAMBDA = 3.55e-5                # 0659 clock cadence, /body/game-s
ITEM_US_X86 = 82.5              # 3aec fired item cost, us x86
X86_TO_M1 = 208 / 355
RTF = 100.0
N9 = 10**9
R_S = 34 * 2.0**-10             # ship radius, root units
D_CONTACT = 2 * R_S             # 0.06640 root = 98.08 m
D_ENC = (1 << 10) * D_CONTACT   # 68.0 root = 100.4 km

# ---- genesis, ported verbatim from scenario.rs (via d4ff work/belt_stream.py) ----

def mix64(z):
    z = (z + 0x9E3779B97F4A7C15) & MASK
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK
    return z ^ (z >> 31)

def draw(seed, k, lane):
    return mix64(mix64(seed ^ 0x5DEECE66D1CE4E5B) ^ ((k * 0x9E3779B97F4A7C15) & MASK) ^ ((lane << 56) & MASK))

def rayleigh_q48(u, sigma_milli):
    d = (1 << 32) - (u & 0xFFFFFFFF)
    k = d.bit_length() - 1
    x = d << (62 - k)
    frac = 0
    for _ in range(32):
        x = (x * x) >> 62
        frac <<= 1
        if x >= (2 << 62):
            x >>= 1
            frac |= 1
    l2 = (32 << 32) - ((k << 32) | frac)
    ln = (l2 * 2_977_044_472) >> 32
    e2 = ((ln * 2 * sigma_milli * sigma_milli) << 64) // 1_000_000
    return math.isqrt(e2)       # e * 2^48

def belt_ship(seed, k):
    d1, d2, d3 = draw(seed, k, 1), draw(seed, k, 2), draw(seed, k, 3)
    a_q8 = ((2 * AU) << 8) + (d1 % ((AU << 8)))
    e = rayleigh_q48((d2 >> 32) & 0xFFFFFFFF, 70)
    lane = 16
    while e > (2 << 48) // 5:
        e = rayleigh_q48((draw(seed, k, lane) >> 32) & 0xFFFFFFFF, 70)
        lane += 1
    p_q8 = a_q8 - ((a_q8 * e) >> 48)
    return a_q8 / 256.0, e / float(1 << 48), p_q8 / 256.0, d3

_HERE = os.path.dirname(os.path.abspath(__file__))

def genesis_table(n=200_000, seed=1, k0=300):
    """(a, e, p, wpi) arrays: a/p in root units, wpi = orientation in [0,2pi)."""
    cache = os.path.join(_HERE, "gen_table.npz")
    if os.path.exists(cache):
        z = np.load(cache)
        if len(z["a"]) == n:
            return z["a"], z["e"], z["p"], z["wpi"]
    a = np.empty(n); e = np.empty(n); p = np.empty(n); w = np.empty(n)
    for i in range(n):
        A, E, P, D3 = belt_ship(seed, k0 + i)
        a[i] = A; e[i] = E; p[i] = P
        w[i] = ((D3 & 0xFFFFFFFF) / 2**32) * 2 * math.pi
    np.savez(cache, a=a, e=e, p=p, wpi=w)
    return a, e, p, w

# ---- closed-form conjunction geometry (the instrument core) ------------------
# Two bodies simultaneously at polar angle th (a conjunction crossing):
#   r_k = p_k / (1 + e_k cos f_k),  f_k = th - wpi_k
#   v_r = e sin f / sqrt(p)  (GM=1, h = sqrt(p)),  v_t = sqrt(p)/r
# separation at the crossing is purely radial: s = (r1-r2) rhat
# relative velocity: dv = (dvr) rhat + (dvt) that  ->  impact parameter
#   b = |s x dv| / |dv| = |dr * dvt| / |dv|
# Straight-line miss valid when |dv| >> Omega*|dr| (curvature negligible over
# the approach); the violating slow tail is quantified separately.

def conj_geom(a1, e1, p1, a2, e2, p2, th, dwpi):
    """b, |dv|, dr, Omega (mean of mean motions, rad/root-time) at crossing th."""
    f1 = th
    f2 = th - dwpi
    r1 = p1 / (1.0 + e1 * np.cos(f1))
    r2 = p2 / (1.0 + e2 * np.cos(f2))
    s1 = 1.0 / np.sqrt(p1); s2 = 1.0 / np.sqrt(p2)
    vr1 = e1 * np.sin(f1) * s1; vt1 = np.sqrt(p1) / r1
    vr2 = e2 * np.sin(f2) * s2; vt2 = np.sqrt(p2) / r2
    dr = r1 - r2
    dvr = vr1 - vr2; dvt = vt1 - vt2
    dv = np.sqrt(dvr * dvr + dvt * dvt)
    b = np.abs(dr * dvt) / np.maximum(dv, 1e-30)
    om = 0.5 * (a1 ** -1.5 + a2 ** -1.5)
    return b, dv, dr, om

def mean_motion(a):
    return a ** -1.5          # rad per root-time (GM = 1)
