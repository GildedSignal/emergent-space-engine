"""Shared pieces for rung r3 v3 (run 20260930-1250-rung-r3-two-body-doll-v3-3565).

Ports, verbatim in formula, from xtask/src/gr_oracle_extended.rs:
  - eih_invariants, damour_deruelle  (the 1PN two-body oracle)
  - bound_constants, bound_period_quad (exact Schwarzschild Darwin quadrature)
and the seed sampler frozen by the rung (Python random.Random(20261002)).
"""
import math
import random

import numpy as np

# ---------------------------------------------------------------- GL quadrature
_GL32_X, _GL32_W = np.polynomial.legendre.leggauss(32)


def integrate_gl(lo, hi, pieces, f):
    """Composite 32-point Gauss-Legendre on `pieces` panels, vectorised."""
    edges = np.linspace(lo, hi, pieces + 1)
    a = edges[:-1][:, None]
    b = edges[1:][:, None]
    x = (a + b) * 0.5 + (b - a) * 0.5 * _GL32_X[None, :]
    w = (b - a) * 0.5 * _GL32_W[None, :]
    return float(np.sum(w * f(x)))


def quad_refine(f, tol=1e-14):
    """Pieces double until converged, as in bound_period_quad (H0193)."""
    pieces = 16
    v = integrate_gl(0.0, 2.0 * math.pi, pieces, f)
    while pieces < 1 << 14:
        pieces *= 2
        w = integrate_gl(0.0, 2.0 * math.pi, pieces, f)
        done = abs(w - v) <= tol * abs(w)
        v = w
        if done:
            break
    return v


# --------------------------------------- exact Schwarzschild (Darwin p, e)
def bound_constants(p, e):
    energy = math.sqrt(((p - 2.0) ** 2 - 4.0 * e * e) / (p * (p - 3.0 - e * e)))
    angular = p / math.sqrt(p - 3.0 - e * e)
    return energy, angular


def schw_advance(p, e):
    """Exact periastron advance per radial period (total azimuth minus 2pi)."""
    return quad_refine(lambda chi: np.sqrt(p / (p - 6.0 - 2.0 * e * np.cos(chi)))) - 2.0 * math.pi


def schw_period_t(p, e):
    """Exact coordinate-time radial period of the bound Schwarzschild geodesic."""
    energy, angular = bound_constants(p, e)

    def dt(chi):
        r = p / (1.0 + e * np.cos(chi))
        dphi = np.sqrt(p / (p - 6.0 - 2.0 * e * np.cos(chi)))
        return dphi * r * r / angular * energy / (1.0 - 2.0 / r)

    return quad_refine(dt)


# ------------------------------------------------- 1PN two-body oracle (port)
def eih_invariants(p, e, nu):
    rp = p / (1.0 + e)
    ra = p / (1.0 - e)
    j0 = math.sqrt(p)

    def correction(r):
        return (-(1.0 - 3.0 * nu) * j0 ** 4 / (8.0 * r ** 4)
                - (3.0 + nu) * j0 * j0 / (2.0 * r ** 3)
                + 1.0 / (2.0 * r * r))

    dj = -(correction(rp) - correction(ra)) / (j0 * (1.0 / (rp * rp) - 1.0 / (ra * ra)))
    vt = (j0 + dj) / rp * (1.0 - 0.5 * (1.0 - 3.0 * nu) * j0 * j0 / (rp * rp) - (3.0 + nu) / rp)
    v2 = vt * vt
    energy = (0.5 * v2 - 1.0 / rp
              + 0.375 * (1.0 - 3.0 * nu) * v2 * v2
              + 0.5 / rp * ((3.0 + nu) * v2 + 1.0 / rp))
    angular = rp * vt * (1.0 + 0.5 * (1.0 - 3.0 * nu) * v2 + (3.0 + nu) / rp)
    return rp, vt, energy, angular


def damour_deruelle(energy, angular, nu):
    q = -2.0 * energy
    n = q ** 1.5 * (1.0 + q * (-15.0 + nu) / 8.0)
    return 6.0 * math.pi / (angular * angular), 2.0 * math.pi / n


def oracle_1pn(p, e, nu):
    """(periastron advance, radial period) from the frozen 1PN oracle."""
    _, _, energy, angular = eih_invariants(p, e, nu)
    return damour_deruelle(energy, angular, nu)


# ------------------------------------------------------------- frozen sampler
def sample_cases():
    """Binaries (1024) then assist impact parameters (64), one Random stream."""
    rng = random.Random(20261002)
    binaries = []
    for _ in range(1024):
        p = math.exp(rng.uniform(math.log(20.0), math.log(1000.0)))
        e = rng.uniform(0.0, 0.6)
        nu = rng.uniform(0.01, 0.25)
        binaries.append((p, e, nu))
    b_rplanet = [math.exp(rng.uniform(math.log(1.5), math.log(50.0))) for _ in range(64)]
    return binaries, b_rplanet


# ----------------------------------------------------- system constants (AU)
AU_KM = 1.495978707e8
V_UNIT = 29.784691831  # km/s: sqrt(GM_sun / 1 AU)
R_PLANET_AU = 6371.0 / AU_KM          # Earth-radius planet
MU_PLANET = 3.0e-6                    # GM in units of GM_star
V_INF = 10.0 / V_UNIT                 # flyby hyperbolic excess speed
R_SOI = MU_PLANET ** 0.4              # a*(m/M)^(2/5) with a = 1 AU
