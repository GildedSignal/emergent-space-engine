"""Shared pieces for rung r9 (Hill regime). Units: G=1, star+planet mass 1,
star-planet separation 1, planet on a circular orbit, n_p = 1.

Sampler (frozen): random.Random(20261010); per seed draw a/R_H ~ U[0.1,0.9],
mean anomaly M0 ~ U[0,2pi], periapsis angle w0 ~ U[0,2pi], in that order;
seeds 0..127 prograde, 128..255 retrograde; e0 = 0.05 for every moon.
tau = (2/3) (r_apo/R_H)^3 with r_apo = a(1+e0).
"""
import numpy as np

MU = 1e-3 / 1.001              # planet mass (star = 1 - MU)
MS = 1.0 - MU
RH = (MU / (3.0 * MS)) ** (1.0 / 3.0)
E0 = 0.05
N_ORB = 50
T_END = 2.0 * np.pi * N_ORB
DT = 0.05                      # sample grid (z is taken every 4th sample)
T_EVAL = np.arange(0.0, T_END + DT / 2, DT)
X_PLANET = 1.0 - MU


def make_seeds():
    import random
    rng = random.Random(20261010)
    seeds = []
    for i in range(256):
        aRH = rng.uniform(0.1, 0.9)
        M0 = rng.uniform(0.0, 2 * np.pi)
        w0 = rng.uniform(0.0, 2 * np.pi)
        seeds.append(dict(i=i, aRH=aRH, M0=M0, w0=w0, retro=(i >= 128), e0=E0))
    return seeds


def kepler_state(a, e, varpi, M, retro, mu=MU):
    """Position/velocity relative to the planet, inertial, from mean anomaly."""
    n = np.sqrt(mu / a ** 3)
    E = M
    for _ in range(100):
        d = -(E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
        E += d
        if abs(d) < 1e-14:
            break
    cE, sE = np.cos(E), np.sin(E)
    xp, yp = a * (cE - e), a * np.sqrt(1 - e * e) * sE
    vxp = -a * n * sE / (1 - e * cE)
    vyp = a * n * np.sqrt(1 - e * e) * cE / (1 - e * cE)
    if retro:
        yp, vyp = -yp, -vyp
    cv, sv = np.cos(varpi), np.sin(varpi)
    return (cv * xp - sv * yp, sv * xp + cv * yp,
            cv * vxp - sv * vyp, sv * vxp + cv * vyp)


def init_state(seed, ascale=1.0):
    """Rotating-frame CR3BP initial state."""
    a = seed["aRH"] * RH * ascale
    x, y, vx, vy = kepler_state(a, seed["e0"], seed["w0"], seed["M0"], seed["retro"])
    return [x + X_PLANET, y, vx + y, vy - x]


def cr3bp(t, s):
    x, y, vx, vy = s
    r1 = np.hypot(x + MU, y)
    r2 = np.hypot(x - X_PLANET, y)
    om1 = (1 - MU) / r1 ** 3
    om2 = MU / r2 ** 3
    return (vx, vy,
            -om1 * (x + MU) - om2 * (x - X_PLANET) + 2 * vy + x,
            -om1 * y - om2 * y - 2 * vx + y)


def rot_to_inert(u_rot, v_rot, t):
    """Relative rotating-frame complex position/velocity -> inertial (n_p=1)."""
    ph = np.exp(1j * t)
    return u_rot * ph, (v_rot + 1j * u_rot) * ph


def osc(uin, vin, mu=MU):
    """Osculating (a, e, z=e*exp(i varpi)) of an inertial relative state."""
    r = np.abs(uin)
    v2 = vin.real ** 2 + vin.imag ** 2
    a = -mu / (v2 - 2.0 * mu / r)
    h = uin.real * vin.imag - uin.imag * vin.real
    ex = vin.imag * h / mu - uin.real / r
    ey = -vin.real * h / mu - uin.imag / r
    e = np.hypot(ex, ey)
    return a, e, ex + 1j * ey
def prec_rate(t, z):
    """Apsidal precession rate over the run: the slope of the unwrapped
    argument of the (secular-smoothed) eccentricity vector z(t)=e exp(i varpi),
    least squares weighted by |z|^2 (near-dips of |z| carry no direction) and
    Caucher-reweighted so that an occasional 2pi unwrap slip cannot bias the
    slope. One identical pipeline for every configuration."""
    ph = np.unwrap(np.angle(z))
    w = np.abs(z) ** 2
    tc = t - t.mean()
    for _ in range(4):
        sw = np.sqrt(w)
        A = np.vstack([tc * sw, sw]).T
        coef, *_ = np.linalg.lstsq(A, ph * sw, rcond=None)
        res = ph - (coef[0] * tc + coef[1])
        sig = 1.4826 * np.median(np.abs(res - np.median(res))) + 1e-9
        w = (np.abs(z) ** 2) / (1.0 + (res / (3 * sig)) ** 2)
    return coef[0]

def secular_z(t, z, width=2 * 2 * np.pi):
    """Suppress the per-orbit (short-period) content of the eccentricity
    vector: two Hann moving averages of `width` (two planet orbits), applied
    identically to every configuration before the precession rate is taken."""
    dt = t[1] - t[0]
    n = int(width / dt) | 1
    w = np.hanning(n)
    w /= w.sum()
    out = z.astype(np.complex128)
    for _ in range(2):
        out = np.convolve(np.pad(out, (n // 2, n // 2), mode="edge"), w, mode="same")[n // 2: n // 2 + len(t)]
    return out
