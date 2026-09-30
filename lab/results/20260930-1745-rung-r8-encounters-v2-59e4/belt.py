"""Rung r8 v2: one doll (dominant mass, mu=1), 2D Newtonian Kepler belt.

Sampler is frozen by the rung: Python random.Random(20261008).
All motion is exact Kepler; elements never change during a run (encounters
are recorded, not applied), so a pair's conjunction geometry repeats.
"""
import math
import random
import numpy as np

TWOPI = 2.0 * np.pi


class Belt:
    def __init__(self, N, sigma_e, rho, a, e, pom, lam0):
        self.N = N
        self.sigma_e = sigma_e
        self.rho = rho
        self.a = np.ascontiguousarray(a, dtype=np.float64)
        self.e = np.ascontiguousarray(e, dtype=np.float64)
        self.pom = np.ascontiguousarray(pom, dtype=np.float64)
        self.lam0 = np.ascontiguousarray(lam0, dtype=np.float64)
        self.n = self.a ** (-1.5)
        self.rlo = self.a * (1.0 - self.e)
        self.rhi = self.a * (1.0 + self.e)


def make_belt(rng: random.Random, N: int, sigma_e: float, rho: float) -> Belt:
    a = np.empty(N); e = np.empty(N); pom = np.empty(N); lam = np.empty(N)
    for k in range(N):
        a[k] = 1.0 + 0.5 * rng.random()
        u = rng.random()          # Rayleigh via inverse transform
        e[k] = sigma_e * math.sqrt(-2.0 * math.log1p(-u))
        pom[k] = TWOPI * rng.random()
        lam[k] = TWOPI * rng.random()
    return Belt(N, sigma_e, rho, a, e, pom, lam)


def belt_params(rng: random.Random):
    """16 belts: sigma_e, rho log-uniform as frozen by the rung."""
    sigma_e = math.exp(rng.uniform(math.log(1e-3), math.log(3e-2)))
    rho = math.exp(rng.uniform(math.log(1e-5), math.log(3e-4)))
    return sigma_e, rho


def kepler_states(t, idx, B, with_v=True):
    """Exact Kepler states for bodies idx at times t (vectorised)."""
    a = B.a[idx]; e = B.e[idx]; n = B.n[idx]
    pom = B.pom[idx]; lam0 = B.lam0[idx]
    M = np.mod(n * t + lam0 - pom, TWOPI)
    E = M.copy()
    for _ in range(6):            # e <= ~0.15: converges to ~1e-15
        E -= (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    c1 = np.sqrt(1.0 - e * e)
    ca = np.cos(E); sa = np.sin(E)
    xp = a * (ca - e); yp = a * c1 * sa
    cp = np.cos(pom); sp = np.sin(pom)
    x = xp * cp - yp * sp
    y = xp * sp + yp * cp
    if not with_v:
        return x, y
    Edot = n / (1.0 - e * ca)
    vxp = -a * sa * Edot; vyp = a * c1 * ca * Edot
    vx = vxp * cp - vyp * sp
    vy = vxp * sp + vyp * cp
    return x, y, vx, vy


def rel_state(t, i, j, B):
    x1, y1, vx1, vy1 = kepler_states(t, i, B)
    x2, y2, vx2, vy2 = kepler_states(t, j, B)
    dx = x1 - x2; dy = y1 - y2
    r1 = np.hypot(x1, y1); r2 = np.hypot(x2, y2)
    # gravitational accelerations (mu = 1) for the Newton derivative
    ax = -x1 / r1**3 + x2 / r2**3
    ay = -y1 / r1**3 + y2 / r2**3
    return dx, dy, vx1 - vx2, vy1 - vy2, ax, ay
