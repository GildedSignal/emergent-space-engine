#!/usr/bin/env python3
"""Red-team falsifier: the two-body doll's strong-field flank.

Candidate (docs/representation.md L37 / docs/law.md L39): the relative orbit of two
comparable masses is a test body in EXACT Schwarzschild with M = m1+m2; nu enters only
through the EOB energy map  Hhat = sqrt(1 + 2 nu (hhat_eff - 1)).
  A_c(u) = 1 - 2u          (exact Schwarzschild g_tt)
  D_c(u) = 1               (exact Schwarzschild A*B, since B = 1/A)

Truth: 2PN EOB (Damour, arXiv:0802.4047, eqs. (16), (20), (21) with the 3PN z3 p^4 term
dropped):
  A_t(u) = 1 - 2u + 2 nu u^3
  D_t(u) = 1 - 6 nu u^2
  hhat_eff = sqrt( (A^2/D) p_r^2 + A (1 + j^2 u^2) ),  Hhat_real = sqrt(1+2nu(hhat-1))

Both share the exact nu=0 limit; the gap between them IS the nu-dependence the doc denies.
Units G=c=M=1, nu = mu/M. Compared at matched real invariants (Hhat, j).

Radial-cycle observables by exact quadrature (endpoint singularity removed by
u = u_a + (u_p-u_a) sin^2(theta), Gauss-Legendre in theta):
  dphi/du = j sqrt(D) / sqrt(W),   W(u) = hhat^2 - A(1 + j^2 u^2)
  dt/du   = Hhat hhat sqrt(D) / (A u^2 sqrt(W))
(nu=0 limits: Darwin's orbit equation and Schwarzschild dt/du exactly.)
"""
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq

GL_N, GL_PAN = 200, 24          # Legendre nodes x panels in theta


import mpmath as mp


def mp_advance(p, e):
    """Independent 40-digit Schwarzschild advance for the V1 anchor (the closed
    form 2pi/sqrt(1-6/p) is only 2PN-accurate; the exact angle is e-dependent)."""
    mp.mp.dps = 30
    p = mp.mpf(p)
    e = mp.mpf(e)
    ua, up = (1 - e) / p, (1 + e) / p
    j2 = p * p / (p - 3 - e * e)
    E2 = (1 - 2 * up) * (1 + j2 * up * up)
    Dl = up - ua

    def W(u):
        return E2 - (1 - 2 * u) * (1 + j2 * u * u)

    def integr(t):
        s = mp.sin(t / 2)
        return mp.sqrt(j2) * (Dl * mp.sin(t) / 2) / mp.sqrt(W(ua + Dl * s * s))
    half = mp.quad(integr, [0, mp.pi / 4, mp.pi / 2, 3 * mp.pi / 4, mp.pi])
    half = half if isinstance(half, mp.mpf) else mp.re(half)
    return float(2 * half - 2 * mp.pi)

def A_of(u, nu, exact):
    return 1.0 - 2.0 * u if exact else 1.0 - 2.0 * u + 2.0 * nu * u**3

def dA_of(u, nu, exact):
    return -2.0 + 0.0 * u if exact else -2.0 + 6.0 * nu * u**2


def D_of(u, nu, exact):
    return 1.0 if exact else 1.0 - 6.0 * nu * u**2


def W_of(u, hhat, j, nu, exact):
    return hhat**2 - A_of(u, nu, exact) * (1.0 + (j * u) ** 2)


def hhat_from_H(Hhat, nu):
    """EOB map inverted: effective energy per reduced mass from real energy per M."""
    return 1.0 + (Hhat**2 - 1.0) / (2.0 * nu)


def H_from_hhat(hhat, nu):
    return np.sqrt(1.0 + 2.0 * nu * (hhat - 1.0))


def turning_points(hhat, j, nu, exact, umax=0.49):
    """Bound-orbit turning points: the FIRST consecutive root pair of W with W>0
    inside (near-horizon allowed regions at larger u are plunge regions)."""
    us = np.linspace(1e-6, umax, 20000)
    W = W_of(us, hhat, j, nu, exact)
    s = np.sign(W)
    roots = []
    for i in np.where(s[:-1] * s[1:] < 0)[0]:
        roots.append(brentq(lambda u: W_of(u, hhat, j, nu, exact), us[i], us[i + 1],
                            xtol=1e-15, rtol=1e-15))
    for i in range(len(roots) - 1):
        um = 0.5 * (roots[i] + roots[i + 1])
        if W_of(um, hhat, j, nu, exact) > 0:
            return roots[i], roots[i + 1]
    return None


def cycle(hhat, j, nu, exact):
    """(dphi_cycle, T_r, u_a, u_p) for one full radial cycle (peri->apo->peri)."""
    tp = turning_points(hhat, j, nu, exact)
    if tp is None:
        return None
    u_a, u_p = tp
    Hhat = H_from_hhat(hhat, nu)
    x, w = leggauss(GL_N)
    dphi = 0.0
    dt = 0.0
    for k in range(GL_PAN):
        a, b = np.pi * k / (2 * GL_PAN), np.pi * (k + 1) / (2 * GL_PAN)
        th = 0.5 * (b - a) * x + 0.5 * (b + a)
        u = u_a + (u_p - u_a) * np.sin(th) ** 2
        sc = np.sin(th) * np.cos(th)
        Q = W_of(u, hhat, j, nu, exact) / ((u_p - u_a) ** 2 * sc**2)
        f = 2.0 / np.sqrt(Q)
        dphi += 0.5 * (b - a) * np.sum(w * f * j * np.sqrt(D_of(u, nu, exact)))
        dt += 0.5 * (b - a) * np.sum(w * f * Hhat * hhat * np.sqrt(D_of(u, nu, exact))
                                     / (A_of(u, nu, exact) * u**2))
    out = (2 * dphi, 2 * dt, u_a, u_p)
    assert np.isfinite(dphi) and np.isfinite(dt), "cycle produced NaN"
    return out


def circular(u, nu, exact):
    """Circular orbit at u: (Hhat, j, Omega_phi) from W=0 and dW/du=0."""
    A, Ap = A_of(u, nu, exact), dA_of(u, nu, exact)
    j2 = -Ap / (Ap * u**2 + 2.0 * A * u)
    if j2 <= 0:
        return None
    j = np.sqrt(j2)
    hhat = np.sqrt(A * (1 + (j * u) ** 2))
    Hhat = H_from_hhat(hhat, nu)
    Omega = A * j * u**2 / (Hhat * hhat)
    return Hhat, j, Omega


def orbit_from_pe(p, e, nu):
    """Real invariants (Hhat, j) such that the CANDIDATE orbit has semi-latus p,
    Newtonian-labelled eccentricity e (exact for the candidate's Schwarzschild W)."""
    if e == 0.0:
        return circular(1.0 / p, nu, True)[:2]
    u_p, u_a = (1 + e) / p, (1 - e) / p
    j2 = 2.0 / ((u_p + u_a) - 2.0 * (u_p**2 + u_p * u_a + u_a**2))
    hhat2 = 1.0 - 2 * u_p + j2 * u_p**2 * (1 - 2 * u_p)
    return H_from_hhat(np.sqrt(hhat2), nu), np.sqrt(j2)


def circ_energy_series(nu, us=(0.004, 0.005, 0.0065, 0.008, 0.010, 0.013, 0.016, 0.020, 0.025, 0.030)):
    """Fit E(x) = -x/2 [1 + a1 x + a2 x^2] from the truth's circular family.
    Conditioned: fit (E*2/(-x) - 1)/x = a1 + a2 x (well-scaled linear fit)."""
    xs, ys = [], []
    for u in us:
        r = circular(u, nu, False)
        if r is None:
            continue
        Hhat, j, Om = r
        x = Om ** (2.0 / 3.0)
        Escaled = -(Hhat - 1.0) / nu / x * 2.0 - 1.0   # = a1 x + a2 x^2
        xs.append(x)
        ys.append(Escaled / x)
    c = np.polyfit(xs, ys, 2)                     # [a3, a2, a1]
    resid = np.max(np.abs(np.polyval(c, xs) - ys))
    return c[2], c[1], resid


def isco(nu, exact, lo=0.05, hi=0.35):
    """Marginal stability: minimum of real Hhat along the circular family (golden)."""
    gr = (np.sqrt(5) - 1) / 2
    a, b = lo, hi

    def f(u):
        r = circular(u, nu, exact)
        return np.inf if r is None else r[0]
    for _ in range(200):
        c, d = b - gr * (b - a), a + gr * (b - a)
        if f(c) < f(d):
            b = d
        else:
            a = c
    return 0.5 * (a + b), f(0.5 * (a + b))


def j_crit_marginal(nu, exact):
    """Critical j at Hhat=1 (marginally bound, B4's scene): double root of W."""
    hhat = hhat_from_H(1.0, nu)

    def gap(u):
        j2 = -dA_of(u, nu, exact) / (dA_of(u, nu, exact) * u**2 + 2 * A_of(u, nu, exact) * u)
        if j2 <= 0:
            return np.nan
        return W_of(u, hhat, np.sqrt(j2), nu, exact)

    us = np.linspace(0.05, 0.45, 4000)
    vals = np.array([gap(u) for u in us])
    for i in range(len(us) - 1):
        if np.isfinite(vals[i]) and np.isfinite(vals[i + 1]) and vals[i] * vals[i + 1] < 0:
            ur = brentq(gap, us[i], us[i + 1], xtol=1e-15)
            j2 = -dA_of(ur, nu, exact) / (dA_of(ur, nu, exact) * ur**2 + 2 * A_of(ur, nu, exact) * ur)
            return ur, np.sqrt(j2)
    return None, None


def gaps(p, e, nu):
    """(advance, advance_gap, period, period_gap, rate_gap) at matched (Hhat, j);
    circular rows compare Omega_phi only."""
    if e == 0.0:
        Hhat, j = orbit_from_pe(p, e, nu)
        u0 = 1.0 / p

        def resid(u):
            r = circular(u, nu, False)
            return np.nan if r is None else (r[0] - Hhat) / Hhat
        us = np.linspace(0.7 * u0, 1.4 * u0, 400)
        vs = [resid(u) for u in us]
        ur = None
        for i in range(len(us) - 1):
            if np.isfinite(vs[i]) and np.isfinite(vs[i + 1]) and vs[i] * vs[i + 1] < 0:
                ur = brentq(resid, us[i], us[i + 1], xtol=1e-14)
                break
        if ur is None:
            return None
        Oc = circular(u0, nu, True)[2]
        Ot = circular(ur, nu, False)[2]
        return None, None, 2 * np.pi / Oc, abs(Ot - Oc) / Ot, abs(Ot - Oc) / Ot
    Hhat, j = orbit_from_pe(p, e, nu)
    h = hhat_from_H(Hhat, nu)
    rc, rt = cycle(h, j, nu, True), cycle(h, j, nu, False)
    if rc is None or rt is None:
        return None
    advc, Tc, advt, Tt = rc[0] - 2 * np.pi, rc[1], rt[0] - 2 * np.pi, rt[1]
    return (advc, abs(advt - advc) / advt, Tc, abs(Tt - Tc) / Tt,
            abs((advt / Tt) - (advc / Tc)) / (advt / Tt))


def main():
    print("=" * 78)
    print("VALIDATION (anchors must pass before any measurement counts)")
    worst, n_v1 = 0.0, 0
    for p in (20.0, 50.0, 100.0):
        for e in (0.3, 0.6):
            Hhat, j = orbit_from_pe(p, e, 1e-8)
            hhat = hhat_from_H(Hhat, 1e-8)
            r = cycle(hhat, j, 1e-8, True)
            dphi = r[0] - 2 * np.pi          # advance beyond 2pi
            anchor = mp_advance(p, e)        # independent 30-digit quadrature
            worst = max(worst, abs(dphi - anchor) / anchor)
            n_v1 += 1
    print(f"V1 candidate(nu=0) vs 30-digit independent quadrature: max rel err = {worst:.3e} "
          f"over {n_v1} orbits (want <2e-6: nu=1e-8 map round-trip noise)")

    worst2 = 0.0
    for u in (0.02, 0.05, 0.1, 0.13):
        Hhat, j, Om = circular(u, 1e-8, True)
        worst2 = max(worst2, abs(Om**2 - u**3) / u**3)
    print(f"V2 candidate(nu=0) circular Omega^2-u^3:  max rel err = {worst2:.3e} (nu=1e-8 cap)")

    a1, a2, res = circ_energy_series(0.25)
    t1, t2 = -3 / 4 - 0.25 / 12, -27 / 8 + 19 * 0.25 / 8 - 0.25**2 / 24
    print(f"V3 truth(0.25) E(x): a1={a1:+.9f} vs {t1:+.9f} | a2={a2:+.9f} vs {t2:+.9f}"
          f" | fit resid {res:.1e} (want: a1<1e-3, a2<1e-2; remainder is fit truncation)")

    # V4: e->0 limit of the eccentric path matches the circular Omega
    Hhat, j = orbit_from_pe(20.0, 0.05, 0.25)
    h = hhat_from_H(Hhat, 0.25)
    rc = cycle(h, j, 0.25, True)
    Om_circ = circular(1.0 / 20.0, 0.25, True)[2]
    print(f"V4 e=0.05: dphi/T_r = {rc[0]/rc[1]:.12f} vs Omega_circ = {Om_circ:.12f} "
          f"(rel {abs(rc[0]/rc[1]-Om_circ)/Om_circ:.1e})")

    print()
    print("=" * 78)
    print("THE FLANK: gaps (truth-candidate)/truth at matched (Hhat, j), nu=0.25")
    print(f"{'p/M':>6} {'e':>4} | {'adv rad':>8} {'gap%':>8} {'B1(1%)':>6} | "
          f"{'per (cand)':>10} {'gap%':>8} {'B2(0.1%)':>8} | {'rate gap%':>9}")
    for p in (100.0, 50.0, 20.0, 12.0):
        for e in (0.0, 0.3, 0.6):
            g = gaps(p, e, 0.25)
            if g is None:
                print(f"{p:6.0f} {e:4.1f} |  (no matching bound orbit)")
                continue
            dpc, gp, Tc, gt, om = g
            adv = (f"{dpc/np.pi:8.4f} {gp*100:8.4f} {'FAIL' if gp > 0.01 else 'ok':>6}"
                   if dpc else f"{'circ':>8} {'--':>8} {'--':>6}")
            print(f"{p:6.0f} {e:4.1f} | {adv} | {Tc:10.4f} {gt*100:8.4f} "
                  f"{'FAIL' if gt > 0.001 else 'ok':>8} | {om*100:9.4f}")

    print()
    print("nu-scaling at p=20, e=0.3 (prediction P5: gaps ~ linear in nu):")
    for nu in (0.25, 0.1):
        g = gaps(20.0, 0.3, nu)
        print(f"  nu={nu:4.2f}: advance gap {g[1]*100:.4f}%   T_r gap {g[3]*100:.4f}%")

    print()
    print("Threshold crossings (nu=0.25, e=0.3), scan p in [8,200]M then bisect:")
    ps = np.linspace(8, 200, 97)
    for thr, which in ((0.01, 0), (0.001, 1)):
        gs = []
        for p in ps:
            g = gaps(p, 0.3, 0.25)
            gs.append(np.nan if g is None else g[1] if which == 0 else g[3])
        gs = np.array(gs)
        cross = [i for i in range(len(ps) - 1)
                 if np.isfinite(gs[i]) and np.isfinite(gs[i + 1])
                 and (gs[i] - thr) * (gs[i + 1] - thr) < 0]

        def gp_at(p):
            g = gaps(p, 0.3, 0.25)
            return (g[1] if which == 0 else g[3]) - thr
        locs = [brentq(gp_at, ps[i], ps[i + 1], xtol=1e-3) for i in cross]
        name = "advance gap" if which == 0 else "T_r gap"
        print(f"  {name} crosses {thr*100:g}% at p ~ "
              + (", ".join(f"{l:.1f}M" for l in locs) if locs else "none in [8,200]"))

    print()
    print("ISCO (circular plunge boundary), prediction P3:")
    for nu in (1e-8, 0.1, 0.25):
        uc, Hc = isco(nu, True)
        ut, Ht = isco(nu, False)
        print(f"  nu={nu:5.2f}: candidate u_ISCO={uc:.6f} (r={1/uc:.3f}M)   "
              f"truth u_ISCO={ut:.6f} (r={1/ut:.3f}M)   radius shift "
              f"{100*(1/uc-1/ut)/(1/ut):+.1f}%")

    print()
    print("Capture boundary at E=1 (B4's scene), prediction P4:")
    for nu in (1e-8, 0.1, 0.25):
        uc, jc = j_crit_marginal(nu, True)
        ut, jt = j_crit_marginal(nu, False)
        print(f"  nu={nu:5.2f}: candidate (u*,j*)=({uc:.4f},{jc:.4f})   "
              f"truth ({ut:.4f},{jt:.4f})   j* gap {100*abs(jt-jc)/jc:.2f}%   "
              f"capture radius gap {100*abs(uc-ut)/ut:.2f}%")


if __name__ == "__main__":
    main()
