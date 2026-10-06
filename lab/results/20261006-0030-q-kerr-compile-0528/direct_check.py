#!/usr/bin/env python3
"""Independent verification of kerr_ref by direct geodesic integration.

No algebra is shared with the compiler: the inverse metric comes from sympy
inverting the equatorial Boyer-Lindquist line element; geodesics are
Hamilton's equations for H = (1/2) g^{mu nu} p_mu p_nu with p_t = -E,
p_phi = L, integrated in the affine parameter (= proper time for mu=1) by
classical RK4 in mpmath, with an h vs h/2 error control. Turning points need
no special handling: p_r crosses zero smoothly. The Hamiltonian value
H + mu^2/2 is monitored as an in-integration error gauge.
"""
import sympy as sp
from mpmath import mp, mpf, sqrt

_r, _a, _E, _L, _pr = sp.symbols("r a E L pr", real=True)

Delta = _r**2 - 2*_r + _a**2
g = sp.Matrix([[-(1 - 2/_r), 0, -2*_a/_r],
               [0, _r**2/Delta, 0],
               [-2*_a/_r, 0, _r**2 + _a**2 + 2*_a**2/_r]])
ginv = sp.simplify(g.inv())
H = sp.Rational(1, 2) * (ginv[0, 0]*_E**2 - 2*ginv[0, 2]*_E*_L
                         + ginv[2, 2]*_L**2 + ginv[1, 1]*_pr**2)
dH_dr = sp.simplify(sp.diff(H, _r))
dt_dlam = sp.simplify(-sp.diff(H, _E))       # dH/dp_t with p_t = -E
dphi_dlam = sp.simplify(sp.diff(H, _L))
dr_dlam = sp.simplify(ginv[1, 1] * _pr)

_F = sp.lambdify((_r, _pr, _a, _E, _L),
                 [dr_dlam, -dH_dr, dt_dlam, dphi_dlam], "mpmath")
_Hval = sp.lambdify((_r, _pr, _a, _E, _L), H, "mpmath")


def rhs(y, a, E, L):
    """Hand-inlined from sympy's CSE of the Hamilton equations (identical
    expressions, fewer generic-lambdify ops; asserted equal in tests)."""
    r, pr = y[0], y[1]
    a2 = a * a
    r2 = r * r
    r3 = r2 * r
    Delta = r2 - 2 * r + a2
    D2 = Delta * Delta
    E2 = E * E
    L2 = L * L
    x9 = E2 * (r * a2 + r3 + 2 * a2)
    x7 = 4 * E * L * a
    x5L2 = L2
    dp = -((2 * pr * pr * D2 * (r - a2)
           + r * Delta * (-L2 * (r - 2) - x7 + x9)
           - r2 * Delta * (-L2 + E2 * (a2 + 3 * r2))
           - 2 * r2 * (r - 1) * (L2 * (r - 2) + x7 - x9)) / (2 * r3 * D2))
    den = r * Delta
    return (Delta / r2 * pr, dp,
            (E * (a2 * r + 2 * a2 + r3) - 2 * L * a) / den,
            (2 * E * a + L * (r - 2)) / den)


def H_value(r, pr, a, E, L):
    return _Hval(r, pr, a, E, L)


def horizon_r(a):
    return 1 + sqrt(1 - a * a)


def _rk4_step(y, h, a, E, L):
    k1 = rhs(y, a, E, L)
    y2 = tuple(y[i] + h / 2 * k1[i] for i in range(4))
    k2 = rhs(y2, a, E, L)
    y3 = tuple(y[i] + h / 2 * k2[i] for i in range(4))
    k3 = rhs(y3, a, E, L)
    y4 = tuple(y[i] + h * k3[i] for i in range(4))
    k4 = rhs(y4, a, E, L)
    return tuple(y[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
                 for i in range(4))


def turning_radii(E, L, a, mu=1):
    """Radii with p_r = 0 (constraint roots), found by a float bracket scan
    plus mpmath bisection. Independent of the compiler's cubic algebra."""
    def constraint(r):
        return H_value(r, 0, a, E, L) + mpf(mu) ** 2 / 2

    r_min = float(horizon_r(a)) * 1.0000001
    hi = 1e7
    roots = []
    n = 3000
    prev_c, prev_r = None, None
    for i in range(n + 1):
        rr = r_min * (hi / r_min) ** (i / n)
        c = float(constraint(rr))
        if prev_c is not None and prev_c * c <= 0:
            lo_, hi_ = prev_r, rr
            for _ in range(120):
                mid = (lo_ + hi_) / 2
                if float(constraint(mid)) * prev_c <= 0:
                    hi_ = mid
                else:
                    lo_ = mid
            roots.append(mpf((lo_ + hi_) / 2))
        prev_c, prev_r = c, rr
    return roots


def integrate_to(E, L, a, mu, y0, lam_end, h0):
    """RK4 from lam=0 (state y0) to lam_end; adaptive h = h0 * (r/10)^1.5
    clipped to [h0/50, 50 h0]. Returns final state."""
    y = tuple(mpf(v) for v in y0)
    lam = mpf(0)
    while lam < lam_end:
        h = min(h0 * (y[0] / 10) ** 1.5, h0 * 50, lam_end - lam)
        if h < h0 / 50:
            h = h0 / 50
        if lam + h > lam_end:
            h = lam_end - lam
        y = _rk4_step(y, h, a, E, L)
        lam += h
    return y


def cycle_increments(E, L, a, mu=1, dps=22, h_scale=0.002):
    """Delta phi, Delta t, Delta tau over one radial period from pericenter.

    h vs h/2 control: the returned values are Richardson-checked; if they
    disagree beyond 1e-13 the step is halved and the run redone.
    """
    old = mp.dps
    mp.dps = dps
    try:
        roots = turning_radii(E, L, a, mu)
        if not roots:
            raise ValueError("no turning point: plunging orbit")
        # V(r) -> -inf at the horizon, so a plunge-branch inner root is
        # always present: the pericenter is the second-smallest root
        # (bound: [r_in, r_peri, r_apo]; unbound: [r_in, r_peri]).
        r_peri = sorted(roots)[1] if len(roots) >= 2 else None
        if r_peri is None or r_peri < horizon_r(a) * 1.0000001:
            raise ValueError("no pericenter outside horizon")
        y0 = (r_peri, 0, 0, 0)
        r_apo = max(roots)

        def run_once(h0):
            y = y0
            lam = mpf(0)
            sign_prev = 1
            crossed_apo = False
            for _ in range(2_000_000):
                h = h0 * max(mpf(10) ** -2, min(mpf(10) ** 2,
                                                (y[0] / 10) ** 1.5))
                y_new = _rk4_step(y, h, a, E, L)
                if y_new[0] < horizon_r(a):
                    raise ValueError("plunged below horizon")
                s_new = 1 if y_new[1] >= 0 else -1
                if s_new < 0:
                    crossed_apo = True
                if crossed_apo and y[1] < 0 <= y_new[1]:
                    # pericenter crossing between y and y_new: refine
                    lo, hi = lam, lam + h
                    yl = y
                    for _ in range(60):
                        mid = (lo + hi) / 2
                        ym = integrate_to(E, L, a, mu, yl, mid - lo,
                                          h0 * 0.5)
                        if ym[1] < 0:
                            lo, yl = mid, ym
                        else:
                            hi = mid
                    y_end = integrate_to(E, L, a, mu, yl,
                                         (lo + hi) / 2 - lo, h0 * 0.25)
                    return {"dphi": y_end[3], "dt": y_end[2],
                            "dtau": (lo + hi) / 2,
                            "H_drift": abs(H_value(y_end[0], y_end[1], a,
                                                   E, L) + mpf(mu) ** 2 / 2)}
                y, lam, sign_prev = y_new, lam + h, s_new
            raise ValueError("radial period not found")

        h0 = h_scale * mpf(r_peri) ** 1.5
        res1 = run_once(h0)
        res2 = run_once(h0 / 2)
        while True:
            worst = max(abs(res2[k] - res1[k]) / max(abs(res1[k]), mpf(1e-3))
                        for k in ("dphi", "dt", "dtau"))
            if worst < mpf(10) ** -13:
                break
            res1, h0 = res2, h0 / 2
            res2 = run_once(h0 / 2)
        res2["step_check"] = worst
        return res2
    finally:
        mp.dps = old


def photon_pass(b, a, r_window=2000.0, dps=22):
    """Total dphi and windowed dt for a photon crossing from r_window back to
    r_window. Independent check of the scattering increments."""
    old = mp.dps
    mp.dps = dps
    try:
        E, L = mpf(1), mpf(b)
        r_w = mpf(r_window)
        # inbound: start at r_window with p_r<0 chosen to satisfy constraint
        def constraint_pr(r):
            # p_r^2 from H = 0 with p_t=-E, p_phi=L
            hh = H_value(r, 0, a, E, L)
            # g^{rr} p_r^2 = -2H - (other terms) => p_r^2 = -(2H)/(g^rr) ... with
            # H(r,0) = other terms, so p_r^2 = -2*(H(r,0)) / g^{rr}... careful:
            # H = 0 = 1/2 (others + g^rr p_r^2) => p_r^2 = -2*H(r,0)/g^rr
            gr = 1 / (r * r / (r * r - 2 * r + a * a))  # g^rr = Delta/r^2
            gr = (r * r - 2 * r + a * a) / (r * r)
            return -2 * hh / gr

        pr2 = constraint_pr(r_w)
        if pr2 <= 0:
            raise ValueError("photon cannot be at that radius")
        pr0 = -sqrt(pr2)

        def run(h0, pr0):
            y = (r_w, pr0, 0, 0)
            lam = mpf(0)
            for _ in range(2_000_000):
                h = h0 * max(mpf(10) ** -2, min(mpf(10) ** 2, (y[0] / 10) ** 1.5))
                y_new = _rk4_step(y, h, a, E, L)
                if y_new[1] > 0 and y[1] <= 0:
                    pass  # pericenter; keep going
                if y_new[0] >= r_w and lam > 0 and y_new[1] > 0:
                    # exited: refine between y and y_new to r = r_w
                    lo, hi = lam, lam + h
                    yl = y
                    for _ in range(60):
                        mid = (lo + hi) / 2
                        ym = integrate_to(E, L, a, 0, yl, mid - lo, h0 * 0.5)
                        if ym[0] < r_w:
                            lo, yl = mid, ym
                        else:
                            hi = mid
                    y_end = integrate_to(E, L, a, 0, yl,
                                         (lo + hi) / 2 - lo, h0 * 0.25)
                    return {"dphi": y_end[3], "dt": y_end[2]}
                y, lam = y_new, lam + h
            raise ValueError("photon did not exit window")

        h0 = mpf(10) ** -3 * mpf(r_window) ** 1.5
        r1 = run(h0, pr0)
        r2 = run(h0 / 2, pr0)
        worst = max(abs(r2[k] - r1[k]) / max(abs(r1[k]), mpf(1))
                    for k in ("dphi", "dt"))
        r2["step_check"] = worst
        return r2
    finally:
        mp.dps = old


def plunge_increments(E, L, a, r_start, dps=22):
    """(dphi, dtau) from r_start (turning point) down to r_+ (1+1e-9),
    by direct RK4; Boyer-Lindquist dt diverges at the horizon (returned None).
    """
    old = mp.dps
    mp.dps = dps
    try:
        rh = horizon_r(a)
        r_end = rh * (1 + mpf(10) ** -9)
        y0 = (mpf(r_start), 0, 0, 0)

        def run(h0):
            y = y0
            lam = mpf(0)
            for _ in range(2_000_000):
                h = h0 * max(mpf(10) ** -3, min(mpf(10) ** 2,
                                                 (y[0] / 10) ** 1.5))
                y_new = _rk4_step(y, h, a, E, L)
                if y_new[0] <= r_end:
                    lo, hi = lam, lam + h
                    yl = y
                    for _ in range(60):
                        mid = (lo + hi) / 2
                        ym = integrate_to(E, L, a, 1, yl, mid - lo, h0 * 0.5)
                        if ym[0] > r_end:
                            lo, yl = mid, ym
                        else:
                            hi = mid
                    y_end = integrate_to(E, L, a, 1, yl,
                                         (lo + hi) / 2 - lo, h0 * 0.25)
                    return {"dphi": y_end[3], "dtau": (lo + hi) / 2,
                            "dt": None, "t_at_end": y_end[2]}
                y, lam = y_new, lam + h
            raise ValueError("did not reach horizon")

        h0 = mpf(10) ** -3
        res1 = run(h0)
        res2 = run(h0 / 2)
        worst = max([abs(res2[k] - res1[k]) / max(abs(res1[k]), mpf(1e-6))
                     for k in ("dphi", "dtau")])
        while worst > mpf(10) ** -13:
            res1, h0 = res2, h0 / 2
            res2 = run(h0 / 2)
            worst = max([abs(res2[k] - res1[k]) / max(abs(res1[k]), mpf(1e-6))
                         for k in ("dphi", "dtau")])
        res2["step_check"] = worst
        return res2
    finally:
        mp.dps = old


if __name__ == "__main__":
    mp.dps = 20
    import kerr_ref as K
    # circular orbit checks against BPT closed forms
    r, chi = 10, 0.5
    E, L = K.circular_EL(r, chi, "pro")
    F = _F(r, 0, mpf(chi), E, L)
    print("dt/dlam:", float(F[2]),
          "formula:", float(1 / sqrt(1 - mpf(3) / r + 2 * mpf(chi) / r ** 1.5)))
    print("Omega:", float(F[3] / F[2]),
          "formula:", float(1 / (mpf(r) ** 1.5 + mpf(chi))))
    print("H + 1/2:", float(H_value(r, 0, mpf(chi), E, L) + mpf(1) / 2))
