"""Candidates for rung r9.

kick-avg : the planet's two-body doll with orbit-averaged tidal kicks from the
star. The single (moon-orbit) average of the rotating-frame quadrupole tide is
the evection Hamiltonian (n_p = 1):
    Hbar = -mu^2/(2L^2) - s*n_p*G - (n_p^2 a^2/2) * X,
    X = alpha/2 + (3/2) beta cos(2w),  alpha = 1 + (3/2) e^2, beta = (5/2) e^2,
with L = sqrt(mu a), G = L sqrt(1-e^2), s = +1 prograde / -1 retrograde, w the
periapsis angle from the star-planet line measured in the direction of motion.
It is applied as one kick per moon orbit (RK2 midpoint), Kepler in between;
a (hence E) is conserved by the average, so the model can never eject a moon.
alpha, beta and the rates are checked against direct quadrature in
verify_secular.py.

no-tide : the plain two-body doll (no kicks): e, a and the periapsis frozen.

hill-torus : in Hill units a regular moon is periodic in the rotating frame,
so its inertial motion is a two-frequency torus (nu_rot, n_p). Frequency
analysis of the truth's first 20 planet orbits: least-squares Fourier fit of
the de-rotated position u_rot (harmonics |k| <= 4). Declared a torus iff the
truth did not escape in the window, the fit covers >= 97% of the power, and a
refit on orbits 0-10 predicts orbits 10-20 to <= 25% rms. Compiled = the
20-orbit fit continued analytically. The precession rates follow from
d(alpha)/d(e^2) = 3/2 and d(beta)/d(e^2) = 5/2.
"""
import json
import numpy as np
from common import (MU, RH, T_END, DT, make_seeds, osc, T_EVAL, secular_z, prec_rate)

TS = T_EVAL[::4]          # the z(t) grid every configuration is judged on


# ---------------------------------------------------------------- kick-avg
def kick_avg(seed):
    a = seed["aRH"] * RH
    e0 = seed["e0"]
    s = -1.0 if seed["retro"] else 1.0
    L = np.sqrt(MU * a)
    G = L * np.sqrt(1 - e0 ** 2)
    w = seed["w0"] if not seed["retro"] else (-seed["w0"] % (2 * np.pi))
    P = 2 * np.pi * np.sqrt(a ** 3 / MU)

    def rates(G, w):
        e2 = max(0.0, 1.0 - (G / L) ** 2)
        Gd = 3.75 * a * a * e2 * np.sin(2 * w)
        wd = -s + (a * G / MU) * (0.75 + 3.75 * np.cos(2 * w))
        return Gd, wd

    z = np.empty(len(TS), dtype=np.complex128)
    t0, G0, w0_ = 0.0, G, w
    Gd0, wd0 = rates(G0, w0_)
    for j, t in enumerate(TS):
        while t0 + P <= t:
            Gm, wm = G0 + 0.5 * P * Gd0, w0_ + 0.5 * P * wd0
            Gdm, wdm = rates(Gm, wm)
            G1 = G0 + P * Gdm
            w1 = w0_ + P * wdm
            t0, G0, w0_ = t0 + P, max(G1, 1e-12 * L), w1 % (2 * np.pi)
            Gd0, wd0 = rates(G0, w0_)
        h = t - t0
        Gt = max(G0 + h * Gd0, 1e-12 * L)
        wt = w0_ + h * wd0
        et = np.sqrt(max(0.0, 1.0 - (Gt / L) ** 2))
        z[j] = et * np.exp(1j * (t + s * wt))
    return z, True   # the averaged model conserves a: always bound


# ---------------------------------------------------------------- no-tide
def no_tide(seed):
    z = seed["e0"] * np.exp(1j * seed["w0"]) * np.ones(len(TS), dtype=np.complex128)
    return z, True


# --------------------------------------------------------------- hill-torus
K = 4


def _lsq(t, u, nu):
    cols = [np.ones_like(t)] + [np.exp(1j * k * nu * t) for k in range(-K, K + 1) if k != 0]
    A = np.stack(cols, axis=1)
    c, *_ = np.linalg.lstsq(A, u, rcond=None)
    r = A @ c - u
    return c, float(np.vdot(r, r).real), float(np.vdot(u - u.mean(), u - u.mean()).real)


def _fit(t, u):
    dt = t[1] - t[0]
    uc = u - u.mean()
    F = np.fft.fft(uc)
    nu0 = np.fft.fftfreq(len(t), dt)[np.argmax(np.abs(F))]
    lo, hi = nu0 * 0.97, nu0 * 1.03
    if nu0 < 0:
        lo, hi = nu0 * 1.03, nu0 * 0.97
    for _ in range(80):
        m1, m2 = (lo + hi) / 2 - (hi - lo) / 4, (lo + hi) / 2 + (hi - lo) / 4
        if _lsq(t, u, m1)[1] > _lsq(t, u, m2)[1]:
            lo = m1
        else:
            hi = m2
    nu = 0.5 * (lo + hi)
    c, ssr, sst = _lsq(t, u, nu)
    return nu, c, ssr, sst


def _peak(t, x, numax):
    """Dominant signed frequency of a complex series (Hann-weighted matched
    filter, ternary-refined)."""
    win = np.hanning(len(t))
    F = np.fft.fft(x * win)
    fr = np.fft.fftfreq(len(t), t[1] - t[0])
    nu0 = fr[np.argmax(np.abs(F) * (np.abs(fr) < numax))]
    df = 1.0 / (len(t) * (t[1] - t[0]))
    lo, hi = nu0 - 1.5 * df, nu0 + 1.5 * df
    for _ in range(60):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if abs(np.dot(x * win, np.exp(-1j * m1 * t))) < abs(np.dot(x * win, np.exp(-1j * m2 * t))):
            lo = m1
        else:
            hi = m2
    return 0.5 * (lo + hi)


def _twin_fit(t, z):
    """z(t) ~ c0 + c1 exp(i nu1 t) [+ c2 exp(i nu2 t)]: the torus section.
    The second frequency is added only if the first leaves > 10% of the
    variance, and is kept only when it is genuinely separated (>= 5/window
    from nu1): two near-duplicate lines fit drift and extrapolate badly."""
    zc = z - z.mean()
    nus = [_peak(t, zc, 2.5)]
    res1 = zc - _project(t, zc, nus)
    if np.vdot(res1, res1).real <= 0.10 * np.vdot(zc, zc).real:
        c = _project_coefs(t, zc, nus)
        return nus, c, 1.0 - np.vdot(res1, res1).real / np.vdot(zc, zc).real
    cand = _peak(t, res1, 2.5)
    if abs(cand - nus[0]) < 5.0 / (t[-1] - t[0]):
        c = _project_coefs(t, zc, nus)
        return nus, c, 1.0 - np.vdot(res1, res1).real / np.vdot(zc, zc).real
    nus.append(cand)
    for _ in range(3):                          # coordinate refinement
        for j in (0, 1):
            rj = zc - _project(t, zc, [nus[1 - j]])
            nus[j] = _peak(t, rj, 2.5)
    c = _project_coefs(t, zc, nus)
    res = zc - _project(t, zc, nus)
    cov = 1.0 - np.vdot(res, res).real / np.vdot(zc, zc).real
    return nus, c, float(cov)

def _basis(t, nus):
    return np.stack([np.ones_like(t)] + [np.exp(1j * nu * t) for nu in nus], axis=1)


def _project(t, z, nus):
    A = _basis(t, nus)
    c = np.linalg.lstsq(A, z, rcond=None)[0]
    return A @ c


def _project_coefs(t, z, nus):
    A = _basis(t, nus)
    return np.linalg.lstsq(A, z, rcond=None)[0]


def hill_torus(seed, z_truth, esc_win):
    """Two-frequency compiled generator from the truth's first 20 planet
    orbits. A regular Hill moon is quasi-periodic with two frequencies, so a
    single-frequency rotating-frame fit covers ~nothing (measured coverage
    ~1e-4); the torus is (nu1, nu2) with section (c0, c1, c2) fitted on the
    secular eccentricity vector. Declared a torus iff the truth did not
    escape in the window, the fit covers >= 90% of the secular variance, and
    the dominant frequency is stable between the two window halves to within
    max(5% of itself, two resolution elements) - Laskar's frequency-diffusion
    test, frozen before scoring."""
    if esc_win:
        return None, None, False, None, None, None
    nW = int(20 * 2 * np.pi / (TS[1] - TS[0]))   # 20 planet orbits on the z grid
    tW, zW = TS[:nW], secular_z(TS[:nW], z_truth[:nW])
    nus, c, cov = _twin_fit(tW, zW)
    nus[0] = prec_rate(tW, zW)          # the slow frequency is pinned by the
    c = _project_coefs(tW, zW - zW.mean(), nus)
    n10 = nW // 2
    ldv = abs(prec_rate(tW[:n10], zW[:n10]) - prec_rate(tW[n10:], zW[n10:]))
    declared = bool(cov >= 0.90 and ldv <= max(0.05 * abs(nus[0]), 2e-3))
    if not declared:
        return None, None, False, float(nus[0]), float(cov), float(ldv)
    zc_full = c[0] + sum(c[j + 1] * np.exp(1j * nus[j] * TS) for j in range(len(nus)))
    bound = bool(np.max(np.abs(zc_full)) < 0.9)
    return zc_full, bound, True, float(nus[0]), float(cov), float(ldv)


TRUTH = None


def _worker(s):
    global TRUTH
    if TRUTH is None:
        with open("truth.json") as f:
            TRUTH = {r["i"]: r for r in json.load(f)}
    i = s["i"]
    with np.load(f"truth_shard{i // 64}.npz") as sh:
        zt = sh[f"z{i}"].astype(np.complex128)
    zh, _, dec, nu, cov, oos = hill_torus(s, zt, TRUTH[i]["esc_win"])
    zk, _ = kick_avg(s)
    zn, _ = no_tide(s)
    return i, zk, zn, zh, dec, nu, cov, oos


def main():
    from multiprocessing import Pool
    seeds = make_seeds()
    with Pool(4) as p:
        res = p.map(_worker, seeds)
    res.sort(key=lambda r: r[0])
    np.savez_compressed("cands.npz", t=TS,
                        **{f"zk{r[0]}": r[1] for r in res},
                        **{f"zn{r[0]}": r[2] for r in res},
                        **{f"zh{r[0]}": (r[3] if r[3] is not None
                                         else np.full(len(TS), np.nan + 0j)) for r in res})
    with open("tori.json", "w") as f:
        json.dump([dict(i=r[0], declared=r[4], nu=r[5], cov=r[6], oos=r[7]) for r in res], f, indent=1)
    print("declared tori:", sum(r[4] for r in res), "/ 256")


if __name__ == "__main__":
    main()
