#!/usr/bin/env python3
"""Surprise-time atlas + kick-cadence experiment for a belt (restricted 3-body).

Scene: star M=1 at origin; planet mass mu on circular orbit a_p=1, n=sqrt(1+mu);
belt bodies massless. Heliocentric coordinates, G=1, times in units of 2pi (planet orbits).

Subcommands:
  selftest - controls: drift exactness, mu=0 no divergence, Jacobi conservation
  atlas    - shadow-pair divergence time T_div(a; mu) via leapfrog
  cadence  - DKD (exact Kepler drift + impulsive planet kick) at k kicks/body-orbit,
             per-body or uniform k, elements vs a converged leapfrog truth
"""
import numpy as np, json, sys, time, os

TWOPI = 2.0 * np.pi
OUT = os.path.dirname(os.path.abspath(__file__))


# ---------------- Stumpff functions ----------------
def stumC(z):
    out = np.empty_like(z)
    p = z > 0
    q = z < 0
    zz = z[p]
    out[p] = (1.0 - np.cos(np.sqrt(zz))) / zz
    zz = -z[q]
    out[q] = (np.cosh(np.sqrt(zz)) - 1.0) / zz
    out[~(p | q)] = 0.5
    return out


def stumS(z):
    out = np.empty_like(z)
    p = z > 0
    q = z < 0
    zz = z[p]
    r = np.sqrt(zz)
    out[p] = (r - np.sin(r)) / (zz * r)
    zz = -z[q]
    r = np.sqrt(zz)
    out[q] = (np.sinh(r) - r) / (zz * r)
    out[~(p | q)] = 1.0 / 6.0
    return out


# ---------------- universal-variable Kepler drift (mu=GM_star=1) ----------------
def drift(r, v, dt):
    """r,v: (n,2) float64; dt: (n,) — propagate each body's Kepler orbit about the star."""
    r0n = np.sqrt((r * r).sum(1))
    v2 = (v * v).sum(1)
    rv = (r * v).sum(1)
    alpha = 2.0 / r0n - v2
    sq = 1.0
    with np.errstate(all="ignore"):
        chi_e = sq * dt * alpha
        ah = np.sqrt(np.maximum(-alpha, 1e-300))
        den = rv + np.sign(dt) * (1.0 / ah) * (1.0 - r0n * alpha)
        chi_h = np.sign(dt) * (1.0 / ah) * np.log(np.maximum((-2.0 * alpha * dt) / den, 1e-300))
        chi_p = sq * dt / r0n
        chi = np.where(alpha > 1e-9, chi_e, np.where(alpha < -1e-9, chi_h, chi_p))
        for _ in range(80):
            z = alpha * chi * chi
            C = stumC(z)
            S = stumS(z)
            F = (rv / sq) * chi * chi * C + (1.0 - r0n * alpha) * chi ** 3 * S + r0n * chi - sq * dt
            dF = (rv / sq) * chi * (1.0 - z * S) + (1.0 - r0n * alpha) * chi * chi * C + r0n
            dchi = F / dF
            chi = chi - dchi
            if np.max(np.abs(dchi)) < 1e-13:
                break
        z = alpha * chi * chi
        C = stumC(z)
        S = stumS(z)
        f = 1.0 - chi * chi / r0n * C
        g = dt - chi ** 3 * sq * S
        rn = f[:, None] * r + g[:, None] * v
        r1n = np.sqrt((rn * rn).sum(1))
        fdot = (sq / (r0n * r1n)) * (alpha * chi ** 3 * S - chi)
        gdot = 1.0 - chi * chi / r1n * C
        v1 = fdot[:, None] * r + gdot[:, None] * v
    return rn, v1, np.max(np.abs(f * gdot - fdot * g - 1.0))


# ---------------- model: star 1 + planet mu (circular, a=1) ----------------
def n_pl(mu):
    return np.sqrt(1.0 + mu)


def a_kep(r):
    rn3 = ((r * r).sum(1)) ** 1.5
    return -r / rn3[:, None]


def a_pert(r, t, mu):
    np_ = n_pl(mu)
    cp, sp = np.cos(np_ * t), np.sin(np_ * t)
    dx = cp - r[:, 0]
    dy = sp - r[:, 1]
    d3 = (dx * dx + dy * dy) ** 1.5
    return mu * np.stack([dx / d3 - cp, dy / d3 - sp], 1)


def a_full(r, t, mu):
    return a_kep(r) + a_pert(r, t, mu)

# ---------------- elements ----------------
def elems(r, v):
    rn = np.sqrt((r * r).sum(1))
    vn2 = (v * v).sum(1)
    rv = (r * v).sum(1)
    a = 1.0 / (2.0 / rn - vn2)
    ex = (vn2 - 1.0 / rn) * r[:, 0] - rv * v[:, 0]
    ey = (vn2 - 1.0 / rn) * r[:, 1] - rv * v[:, 1]
    e = np.sqrt(ex * ex + ey * ey)
    w = np.arctan2(ey, ex)
    return a, e, w


def init_belt(a0, e0, w0, M0):
    """heliocentric state from (a, e, varpi, mean anomaly)."""
    E = M0 + e0 * np.sin(M0)
    for _ in range(50):
        E = E - (E - e0 * np.sin(E) - M0) / (1.0 - e0 * np.cos(E))
    cE, sE = np.cos(E), np.sin(E)
    x = a0 * (cE - e0)
    y = a0 * np.sqrt(1.0 - e0 * e0) * sE
    n = a0 ** -1.5
    edx = -sE / (1 - e0 * cE)
    edy = np.sqrt(1.0 - e0 * e0) * cE / (1 - e0 * cE)
    vx = a0 * n * edx
    vy = a0 * n * edy
    cw, sw = np.cos(w0), np.sin(w0)
    r = np.stack([x * cw - y * sw, x * sw + y * cw], 1)
    v = np.stack([vx * cw - vy * sw, vx * sw + vy * cw], 1)
    return r, v


def jacobi(r, v, t, mu):
    """CRTBP Jacobi constant in the uniformly rotating barycentric frame.
    Model: star mass 1 (heliocentric origin), planet mu at radius 1, n=sqrt(1+mu)."""
    n = n_pl(mu)
    c = np.stack([np.broadcast_to(np.cos(n * t), r.shape[:1]), np.broadcast_to(np.sin(n * t), r.shape[:1])], 1)
    xb = r - mu * c
    vbi = v - mu * n * np.stack([-c[:, 1], c[:, 0]], 1)      # v_star-orbit term
    u = vbi - n * np.stack([-xb[:, 1], xb[:, 0]], 1)          # rotating-frame velocity
    r1 = np.sqrt((r * r).sum(1))
    d2 = r - c
    r2 = np.sqrt((d2 * d2).sum(1))
    return (n * n) * ((xb * xb).sum(1)) + 2.0 * (1.0 / r1 + mu / r2) - (u * u).sum(1)


# ---------------- atlas: shadow divergence ----------------
def atlas(a_bins, phases, mu, T_orb, sample_every=4, d_target=1e-3, d0=1e-8, hdiv=64, seed=20261008):
    rng = np.random.default_rng(seed)
    a0 = np.repeat(a_bins, phases)
    nb = a0.size
    e0 = np.zeros(nb)
    w0 = rng.uniform(0, TWOPI, nb)
    M0 = rng.uniform(0, TWOPI, nb)
    r, v = init_belt(a0, e0, w0, M0)
    r2, v2 = init_belt(a0, e0, w0, M0 + d0)
    h = TWOPI / hdiv
    nst = int(T_orb * hdiv)
    tdiv = np.full(nb, np.inf)
    prevd = np.full(nb, d0)
    tprev = np.zeros(nb)
    t = 0.0
    t0 = time.time()
    for i in range(nst):
        v = v + 0.5 * h * a_full(r, t, mu)
        v2 = v2 + 0.5 * h * a_full(r2, t, mu)
        r = r + h * v
        r2 = r2 + h * v2
        t += h
        v = v + 0.5 * h * a_full(r, t, mu)
        v2 = v2 + 0.5 * h * a_full(r2, t, mu)
        if (i + 1) % sample_every == 0:
            d = np.sqrt(((r - r2) ** 2).sum(1)) / a0
            hit = (d >= d_target) & np.isinf(tdiv)
            if hit.any():
                frac = np.log(d_target / prevd[hit]) / np.log(d[hit] / prevd[hit])
                tdiv[hit] = tprev[hit] + frac * (t - tprev[hit])
            prevd = np.where(d < d_target, d, prevd)
            tprev = np.where(np.isinf(tdiv), t, tprev)
    return dict(a=a0, tdiv=tdiv, mu=mu, T_orb=T_orb, wall=time.time() - t0,
                hdiv=hdiv, d_target=d_target, d0=d0)


# ---------------- cadence: DKD Kepler drift + impulsive kicks ----------------
def cadence_run(a0, e0, w0, M0, mu, T_orb, kvec, track_every=None):
    """kvec: kicks per body's own radial period (n,). DKD: kick half, exact Kepler
    drift, kick half. Planet position evaluated at each body's own epoch."""
    r, v = init_belt(a0, e0, w0, M0)
    n = a0.size
    P = TWOPI * a0 ** 1.5
    h = P / kvec
    t = np.zeros(n)
    act = np.ones(n, bool)
    t0 = time.time()
    snaps = []  # (orbit count, max |dC| vs initial per body at snapshots)
    Cj0 = jacobi(r, v, 0.0, mu)
    step_count = 0
    while act.any():
        idx = np.nonzero(act)[0]
        ri, vi, hi, ti = r[idx], v[idx], h[idx], t[idx]
        vi = vi + 0.5 * hi[:, None] * a_pert(ri, ti, mu)
        ri, vi, _ = drift(ri, vi, hi)
        ti = ti + hi
        vi = vi + 0.5 * hi[:, None] * a_pert(ri, ti, mu)
        r[idx], v[idx], t[idx] = ri, vi, ti
        step_count += 1
        done = t >= T_orb * TWOPI
        act[done] = False
        if track_every is not None and step_count % track_every == 0:
            snaps.append((step_count, np.max(np.abs(jacobi(ri, vi, ti, mu) - Cj0[idx]))))
    a, e, w = elems(r, v)
    Cj = jacobi(r, v, t, mu)
    return dict(a=a, e=e, w=w, Cj=Cj, t=t, wall=time.time() - t0, snaps=snaps)


def leapfrog_truth(a0, e0, w0, M0, mu, T_orb, hdiv=1024):
    r, v = init_belt(a0, e0, w0, M0)
    h = TWOPI / hdiv
    nst = int(T_orb * hdiv)
    t = 0.0
    t0 = time.time()
    for i in range(nst):
        v += 0.5 * h * a_full(r, t, mu)
        r += h * v
        t += h
        v += 0.5 * h * a_full(r, t, mu)
    a, e, w = elems(r, v)
    Cj = jacobi(r, v, t, mu)
    return dict(a=a, e=e, w=w, Cj=Cj, t=t, wall=time.time() - t0)


# ---------------- selftest ----------------
def selftest():
    rng = np.random.default_rng(1)
    a0 = rng.uniform(0.5, 2.0, 500)
    e0 = rng.uniform(0.0, 0.4, 500)
    w0 = rng.uniform(0, TWOPI, 500)
    M0 = rng.uniform(0, TWOPI, 500)
    r, v = init_belt(a0, e0, w0, M0)
    P = TWOPI * a0 ** 1.5
    r1, v1, fg = drift(r, v, P)
    dpos = np.sqrt(((r1 - r) ** 2).sum(1))
    E0 = ((v * v).sum(1)) / 2 - 1.0 / np.sqrt((r * r).sum(1))
    E1 = ((v1 * v1).sum(1)) / 2 - 1.0 / np.sqrt((r1 * r1).sum(1))
    print("fg unit err %.2e  period-close frac %.3f  max|dE| %.2e" %
          (fg, np.mean(dpos < 1e-6), np.max(np.abs(E1 - E0))))
    vh = v * 3.0
    r2, v2, fg2 = drift(r, vh, np.full_like(P, 0.7))
    E0h = ((vh * vh).sum(1)) / 2 - 1.0 / np.sqrt((r * r).sum(1))
    E1h = ((v2 * v2).sum(1)) / 2 - 1.0 / np.sqrt((r2 * r2).sum(1))
    print("hyper fg %.2e max|dE| %.2e" % (fg2, np.max(np.abs(E1h - E0h))))
    res = atlas(np.array([0.7, 1.3, 0.85]), 2, 0.0, 200, 8)
    print("mu=0 tdiv finite:", np.sum(np.isfinite(res["tdiv"])), "of", res["tdiv"].size)
    mu = 1e-3
    a2 = np.full(2, 0.75)
    r3, v3 = init_belt(a2, np.full(2, 0.05), np.full(2, 0.3), np.full(2, 1.0))
    cj0 = jacobi(r3, v3, 0.0, mu)
    for hdiv in [1024, 2048, 4096]:
        rr, vv = r3.copy(), v3.copy()
        hh = TWOPI / hdiv
        t = 0.0
        mx = 0.0
        for i in range(hdiv * 50):
            vv += 0.5 * hh * a_full(rr, t, mu)
            rr += hh * vv
            t += hh
            vv += 0.5 * hh * a_full(rr, t, mu)
            if (i + 1) % 512 == 0:
                mx = max(mx, np.max(np.abs(jacobi(rr, vv, t, mu) - cj0)))
        print("hdiv=%5d  max|dC| over 50 orbits: %.3e" % (hdiv, mx))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "selftest"
    if cmd == "selftest":
        selftest()
