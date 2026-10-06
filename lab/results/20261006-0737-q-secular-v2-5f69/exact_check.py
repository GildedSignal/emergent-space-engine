"""Truth verification for run 20261006-0737-q-secular-v2-5f69.

The belt is massless, so the planets' evolution in the full WH truth is IDENTICAL to
the planets-only problem. Chain of checks (bars stated in predictions.md):
  0. drift_fg (Gauss f/g) vs DOP853 on the pure two-body problem: machine precision.
  A. exact heliocentric DOP853 vs exact barycentric DOP853 (different coordinates,
     different code): tolerance ladder separates unconverged numerics from chaos.
  B. planets-only WH (hand-coded DKD with the FIXED kick) at h = 0.125 and h = 0.1875
     vs exact: discretization error must shrink with h; horizon-limited if chaotic.
  C. LL drivers: z_P(t) from the run-008e alpha^2 matrix vs the corrected matrix
     (inner row alpha^2 b, outer row alpha b) against exact z_P(t): settles the
     alpha power empirically. Reported, not graded.
  D. quadrupole-limit sanity: b_{3/2}^{(1)}(alpha) ~ 3 alpha at the scene's alpha.

zvec uses GM = 1 (same convention as wh_run.elements) for BOTH exact and WH
planets, so the O(m) convention offset cancels in every comparison below.
"""
import math
import time

import numpy as np
from scipy.integrate import solve_ivp

import wh_run as W

T = 149022.4
NSTOR = W.NSTOR
stor_times = np.linspace(0, T, NSTOR + 1)[1:]
M_J, M_S = W.MU_J, W.MU_S


def init_planets():
    """Osculating (a,e,varpi,M=0) -> heliocentric Cartesian, mu-consistent (as fixed)."""
    out = []
    for (a, e, wp, m) in [(W.A_J, W.E_J, W.VARPI_J, M_J), (W.A_S, W.E_S, W.VARPI_S, M_S)]:
        mu = 1.0 + m
        n = math.sqrt(mu / a ** 3)
        E = 0.0  # M = 0
        x, y = a * (math.cos(E) - e), a * math.sqrt(1 - e * e) * math.sin(E)
        Edot = n / (1 - e * math.cos(E))
        vx, vy = -a * math.sin(E) * Edot, a * math.sqrt(1 - e * e) * math.cos(E) * Edot
        c, s = math.cos(wp), math.sin(wp)
        r = np.array([c * x - s * y, s * x + c * y])
        v = np.array([c * vx - s * vy, s * vx + c * vy])
        out.append((r, v))
    return out


def zvec(r, v):
    rn = np.linalg.norm(r)
    hz = r[0] * v[1] - r[1] * v[0]
    ex = v[1] * hz - r[0] / rn
    ey = -v[0] * hz - r[1] / rn
    return ex + 1j * ey


def rhs_helio(t, y):
    # state: [rJ(0:2) vJ(2:4) rS(4:6) vS(6:8)]
    rJ, vJ, rS, vS = y[0:2], y[2:4], y[4:6], y[6:8]
    d = rS - rJ
    dn = np.linalg.norm(d)
    rJn = np.linalg.norm(rJ)
    rSn = np.linalg.norm(rS)
    # exact heliocentric reduction of the full Newtonian problem (== WH's h->0 limit):
    # -(1+m_i) r_i/|r_i|^3 + sum_{j != i} m_j [ (r_j - r_i)/|.|^3 - r_j/|r_j|^3 ]
    # (the -m_i term completes the indirect sum over ALL planets; dropping it was the
    # 8.4e-3 helio-vs-bary gap found by the ladder)
    aJ = -(1 + M_J) * rJ / rJn ** 3 + M_S * (d / dn ** 3 - rS / rSn ** 3)
    aS = -(1 + M_S) * rS / rSn ** 3 + M_J * (-d / dn ** 3 - rJ / rJn ** 3)
    return np.concatenate([vJ, aJ, vS, aS])


def rhs_bary(t, y):
    # state: [rs(0:2) vs(2:4) rJ(4:6) vJ(6:8) rS(8:10) vS(10:12)]
    R = [y[0:2], y[4:6], y[8:10]]
    V = [y[2:4], y[6:8], y[10:12]]
    m = [1.0, M_J, M_S]
    acc = []
    for i in range(3):
        a = np.zeros(2)
        for j in range(3):
            if i != j:
                d = R[j] - R[i]
                a += m[j] * d / np.linalg.norm(d) ** 3
        acc.append(a)
    return np.concatenate([V[0], acc[0], V[1], acc[1], V[2], acc[2]])


def exact_helio_tol(rtol=1e-12, atol=1e-14):
    (rJ, vJ), (rS, vS) = init_planets()
    y0 = np.concatenate([rJ, vJ, rS, vS])
    sol = solve_ivp(rhs_helio, (0, T), y0, method="DOP853", rtol=rtol, atol=atol,
                    t_eval=stor_times)
    assert sol.success
    zj = np.array([zvec(sol.y[0:2, i], sol.y[2:4, i]) for i in range(sol.y.shape[1])])
    zs = np.array([zvec(sol.y[4:6, i], sol.y[6:8, i]) for i in range(sol.y.shape[1])])
    return zs, zj, sol


def exact_bary_tol(rtol=1e-13, atol=1e-15):
    (rJ, vJ), (rS, vS) = init_planets()
    Mtot = 1.0 + M_J + M_S
    rs = -(M_J * rJ + M_S * rS) / Mtot
    vs = -(M_J * vJ + M_S * vS) / Mtot
    y0 = np.concatenate([rs, vs, rs + rJ, vs + vJ, rs + rS, vs + vS])
    sol = solve_ivp(rhs_bary, (0, T), y0, method="DOP853", rtol=rtol, atol=atol,
                    t_eval=stor_times)
    assert sol.success
    zj = np.array([zvec(sol.y[4:6, i] - sol.y[0:2, i], sol.y[6:8, i] - sol.y[2:4, i])
                   for i in range(sol.y.shape[1])])
    zs = np.array([zvec(sol.y[8:10, i] - sol.y[0:2, i], sol.y[10:12, i] - sol.y[2:4, i])
                   for i in range(sol.y.shape[1])])
    return zs, zj


def drift_selftest():
    """drift_fg vs DOP853 on the pure two-body problem, random BOUND states."""
    rng = np.random.default_rng(7)
    N = 64
    r = rng.uniform(-2, 2, (N, 2)) + np.array([4.0, 0.0])
    d = rng.uniform(-1, 1, (N, 2))
    vc = np.sqrt(1.0 / np.linalg.norm(r, axis=1))[:, None]          # GM = 1
    v = 0.6 * vc * (d / np.linalg.norm(d, axis=1)[:, None])         # bound: 0.6 x circ
    mu = 1.0 + 9.5e-4
    h = 0.25
    r2, v2_ = drift_fg(r.copy(), v.copy(), h, np.full(N, mu))
    err = 0.0
    for i in range(N):
        sol = solve_ivp(lambda t, y: np.concatenate([y[2:4], -mu * y[0:2] /
                                                     np.linalg.norm(y[0:2]) ** 3]),
                        (0, h), np.concatenate([r[i], v[i]]), method="DOP853",
                        rtol=1e-13, atol=1e-14)
        err = max(err, np.linalg.norm(sol.y[0:2, -1] - r2[i]),
                  np.linalg.norm(sol.y[2:4, -1] - v2_[i]))
    return err


def drift_fg(r, v, h, mu):
    """Exact two-body drift (Gauss f/g via Newton on the generalized anomaly)."""
    rn = np.linalg.norm(r, axis=1)
    v2 = (v * v).sum(1)
    aa = 1 / (2 / rn - v2 / mu)
    nn = np.sqrt(mu / aa ** 3)
    sig = (r * v).sum(1) / np.sqrt(mu * aa)
    ec, es = 1 - rn / aa, sig
    dM = nn * h
    x = dM.copy()
    for _ in range(15):
        s, c = np.sin(x), np.cos(x)
        x -= (x - ec * s + es * (1 - c) - dM) / (1 - ec * c + es * s)
    s, c = np.sin(x), np.cos(x)
    f = aa / rn * (c - 1) + 1
    g = h + (s - x) / nn
    r2 = f[:, None] * r + g[:, None] * v
    r2n = np.linalg.norm(r2, axis=1)
    fd = -aa * aa * nn * s / (r2n * rn)
    gd = aa / r2n * (c - 1) + 1
    return r2, fd[:, None] * r + gd[:, None] * v


def wh_planets(h):
    """Planets-only WH with the FIXED kick (same equations as wh_run.accel v2).
    Returns (z_S, z_J) at the 384 stored times."""
    (rJ, vJ), (rS, vS) = init_planets()
    r = np.array([rJ, rS])
    v = np.array([vJ, vS])
    mu = np.array([1.0 + M_J, 1.0 + M_S])
    mp = [M_J, M_S]

    def accel(r):
        # a_i = sum_{j != i} m_j [ (r_j - r_i)/|r_j - r_i|^3 - r_j/|r_j|^3 ]
        out = np.zeros_like(r)
        for j in (0, 1):
            i = 1 - j
            d = r[j] - r[i]
            out[i] += mp[j] * (d / np.linalg.norm(d) ** 3
                               - r[j] / np.linalg.norm(r[j]) ** 3)
        return out

    nsteps = int(round(T / h))
    zs = np.zeros(NSTOR, complex)
    zj = np.zeros(NSTOR, complex)
    si = 0
    t = 0.0
    for step in range(nsteps):
        r, v = drift_fg(r, v, h / 2, mu)
        v = v + h * accel(r)
        r, v = drift_fg(r, v, h / 2, mu)
        t += h
        if si < NSTOR and t >= stor_times[si] - h / 2:
            zs[si] = zvec(r[1], v[1])
            zj[si] = zvec(r[0], v[0])
            si += 1
    assert si == NSTOR
    return zs, zj


def ll_planet_z(t, matrix):
    """z_P(t) from an LL matrix and initial planet z."""
    g, V = np.linalg.eig(matrix)
    g = g.real
    o = np.argsort(g)
    g, V = g[o], V[:, o]
    z0 = np.array([W.E_J * np.exp(1j * W.VARPI_J), W.E_S * np.exp(1j * W.VARPI_S)])
    c = np.linalg.solve(V, z0)
    e = np.exp(1j * np.outer(t, g))
    return np.einsum("pk,tk->tp", (V * c), e), g


def matrices():
    from wh_run import laplace_b, A_J, A_S
    al = A_J / A_S
    nJ, nS = A_J ** -1.5, A_S ** -1.5
    b1, b2 = laplace_b(1.5, 1, al), laplace_b(1.5, 2, al)
    M_old = np.zeros((2, 2))
    M_new = np.zeros((2, 2))
    for i, j in [(0, 1), (1, 0)]:
        mj = M_S if j == 1 else M_J
        for M, pa in [(M_old, al * al), (M_new, al * al if i == 0 else al)]:
            pref = [nJ, nS][i] * mj / 4 * pa
            M[i, i] += pref * b1
            M[i, j] = -pref * b2
    return M_old, M_new


def main():
    ARCSEC = 206265 * 2 * math.pi
    t0 = time.time()
    print(f"[0] drift self-test vs DOP853 (two-body): max err = {drift_selftest():.2e}")
    zS_hel, zJ_hel, sol = exact_helio_tol()
    zS_bar, zJ_bar = exact_bary_tol()
    print(f"[A] exact-vs-exact: max|dz_S|={np.abs(zS_hel - zS_bar).max():.2e} "
          f"max|dz_J|={np.abs(zJ_hel - zJ_bar).max():.2e} "
          f"(nfev={sol.nfev}, {time.time()-t0:.0f}s)")
    print(f"    exact |z_S|: start {np.abs(zS_hel[0]):.4f} min {np.abs(zS_hel).min():.4f} "
          f"@t={stor_times[np.argmin(np.abs(zS_hel))]:.0f} end {np.abs(zS_hel[-1]):.4f}")
    print(f"    exact |z_J|: start {np.abs(zJ_hel[0]):.4f} end {np.abs(zJ_hel[-1]):.4f} "
          f"max {np.abs(zJ_hel).max():.4f}")

    for h in (0.1875, 0.125):
        zs, zj = wh_planets(h)
        dS = np.abs(zs - zS_hel).max()
        dJ = np.abs(zj - zJ_hel).max()
        print(f"[B] WH h={h}: max|dz_S|={dS:.2e} max|dz_J|={dJ:.2e} ({time.time()-t0:.0f}s)")

    M_old, M_new = matrices()
    z_old, g_old = ll_planet_z(stor_times, M_old)
    z_new, g_new = ll_planet_z(stor_times, M_new)
    print(f"[C] LL g: old(a^2/a^2) = {g_old * ARCSEC:.2f} \"/yr; "
          f"new(a^2/a) = {g_new * ARCSEC:.2f} \"/yr")
    for nm, zll in (("old", z_old), ("new", z_new)):
        dS = np.abs(zll[:, 1] - zS_hel).max()
        dJ = np.abs(zll[:, 0] - zJ_hel).max()
        print(f"    LL-{nm} vs exact: max|dz_S|={dS:.4f} |z_S|(T)={np.abs(zll[-1, 1]):.4f} "
              f"max|dz_J|={dJ:.4f} |z_J|(T)={np.abs(zll[-1, 0]):.4f}")
    print(f"    exact |z_S|(T)={np.abs(zS_hel[-1]):.4f} |z_J|(T)={np.abs(zJ_hel[-1]):.4f}")
    from wh_run import laplace_b
    al = W.A_J / W.A_S
    print(f"[D] b_3/2^1(a)/3a at a={al:.3f}: {laplace_b(1.5, 1, al) / (3 * al):.3f} "
          f"(quadrupole asymptote -> 1)")


if __name__ == "__main__":
    main()
