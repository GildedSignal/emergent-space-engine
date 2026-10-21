#!/usr/bin/env python3
"""The multiply-add cycle certificate (representation.md L67) on the exact Schwarzschild cycle map.

Premise under test (docs/representation.md, section 3):
    "A cycle's derivatives are stored with it, so a kick updates the cycle by a multiply-add."
The cycle of a doll orbit is (dphi, dt, dtau) per radial cycle, functions of the invariants (E, L).
A kick changes (E, L). The premise says the stored cycle is updated by ONE multiply-add with the
derivatives stored at derivation time, until the next derivation. The certificate is the number of
kicks N* over which that linear description reproduces the exact map within a behaviour bar.

Exact map: Schwarzschild geodesic, M = 1, per-unit-mass invariants E (energy), L (angular momentum).
    (dr/dtau)^2 = E^2 - V(r),  V(r) = (1 - 2/r)(1 + L^2/r^2)
    u = 1/r; roots of E^2 = V(u): u_a (apocentre), u_p (pericentre), u_x (unphysical, u_x > u_p).
    E^2 - V(u) = 2 L^2 (u - u_a)(u_p - u)(u_x - u).
    Substitution u = u_a + (u_p - u_a) sin^2 t removes both endpoint square roots; the integrands
    are smooth on [0, pi/2]:
        dphi = 2 sqrt(2) * INT dt / sqrt(u_x - u(t))
        dtau = (2 sqrt(2)/L) * INT dt / (u(t)^2 sqrt(u_x - u(t)))
        dt   = (2 sqrt(2) E/L) * INT dt / (u(t)^2 (1-2u(t)) sqrt(u_x - u(t)))
Controls: weak-field pericentre advance dphi - 2pi -> 6 pi / pbar (O(pbar^-2) residual); Kepler
dt -> 2 pi pbar^{3/2} / (1-e^2)^{3/2}; factorisation asserted numerically.
"""
import json
import math
import sys
import numpy as np
from scipy.integrate import quad

SQ2 = math.sqrt(2.0)
EPSREL = 1e-12
EPSABS = 1e-14

def roots_from_pbar_e(pbar, e):
    """(E, L, u_p, u_a, u_x) in the Darwin (p, e) convention: r_p = p/(1+e), r_a = p/(1-e).
    Exact Schwarzschild: L^2 = p^2 / (p - 3 - e^2); separatrix p = 6 + 2e; third root
    u_x = 1/2 - u_p - u_a exactly (Vieta: sum of roots of 2L^2 u^3 - L^2 u^2 + 2u + (E^2-1))."""
    if pbar <= 6.0 + 2.0 * e:
        raise ValueError("past the separatrix: pbar=%.6g e=%.6g (6+2e=%.6g)" % (pbar, e, 6 + 2 * e))
    L = pbar / math.sqrt(pbar - 3.0 - e * e)
    u_p = (1.0 + e) / pbar
    u_a = (1.0 - e) / pbar
    E2 = (1.0 - 2.0 * u_p) * (1.0 + L * L * u_p * u_p)
    E = math.sqrt(E2)
    if not (E < 1.0):
        raise ValueError("not bound: E=%.6g pbar=%.6g e=%.6g" % (E, pbar, e))
    u_x = 0.5 - u_p - u_a
    if not (u_x > u_p):
        raise ValueError("u_x <= u_p (past the separatrix): pbar=%.6g e=%.6g" % (pbar, e))
    # control: u_a must be a turning point of the same (E, L)
    E2a = (1.0 - 2.0 * u_a) * (1.0 + L * L * u_a * u_a)
    if abs(E2a - E2) > 1e-12 * E2:
        raise AssertionError("u_a not a root: E2(a)=%.17g E2(p)=%.17g" % (E2a, E2))
    return E, L, u_p, u_a, u_x


def roots_from_EL(E, L):
    """(u_p, u_a, u_x) from invariants, by bracketed root-finding on f(u) = E^2 - V(u)
    (np.roots loses the small turning points at weak field: coefficient spread 2e10).
    Returns None past a type boundary (unbound, plunging, or at the separatrix)."""
    L2 = L * L
    grid = np.linspace(0.0, 0.5, 200001)[1:]
    f = E * E - (1.0 - 2.0 * grid) * (1.0 + L2 * grid * grid)
    nz = np.nonzero(f)[0]
    if len(nz) < 2:
        return None
    sg = np.sign(f[nz])
    ch = np.nonzero(sg[:-1] != sg[1:])[0]
    from scipy.optimize import brentq

    def fu(u):
        return E * E - (1.0 - 2.0 * u) * (1.0 + L2 * u * u)

    roots = [float(grid[i]) for i in np.nonzero(f == 0.0)[0]]  # exact hits
    for k in ch:
        i, j = int(nz[k]), int(nz[k + 1])
        roots.append(brentq(fu, grid[i], grid[j], xtol=1e-18, rtol=8.9e-16, maxiter=200))
    roots = sorted(roots)
    # dedupe near-coincident roots
    dedup = []
    for r in roots:
        if not dedup or abs(r - dedup[-1]) > 1e-6 * max(r, 1e-3):
            dedup.append(r)
    roots = dedup
    if len(roots) != 3:
        return None  # plunging/marginal (type boundary)
    u_a, u_p, u_x = roots
    if u_x - u_p < 1e-12 * u_x:
        return None  # at the separatrix
    if abs(u_a + u_p + u_x - 0.5) > 1e-9 * 0.5:
        raise AssertionError("Vieta violated: %.17g" % (u_a + u_p + u_x))
    return u_p, u_a, u_x


def _check_factor(E, L, u_p, u_a, u_x):
    u = 0.5 * (u_a + u_p)
    lhs = E * E - (1.0 - 2.0 * u) * (1.0 + L * L * u * u)
    rhs = 2.0 * L * L * (u - u_a) * (u_p - u) * (u_x - u)
    if abs(lhs - rhs) > 1e-9 * abs(lhs) + 1e-15:
        raise AssertionError("factorisation broken: %.3e vs %.3e" % (lhs, rhs))

def cycle_from_roots(E, L, u_p, u_a, u_x):
    """Exact (dphi, dt, dtau) for one full radial cycle (pericentre to pericentre)."""
    _check_factor(E, L, u_p, u_a, u_x)
    d = u_p - u_a

    def u_of(t):
        return u_a + d * math.sin(t) * math.sin(t)

    def g_phi(t):
        return 1.0 / math.sqrt(u_x - u_of(t))

    def g_tau(t):
        u = u_of(t)
        return 1.0 / (u * u * math.sqrt(u_x - u))

    def g_t(t):
        u = u_of(t)
        return 1.0 / (u * u * (1.0 - 2.0 * u) * math.sqrt(u_x - u))

    I_phi = quad(g_phi, 0.0, math.pi / 2.0, epsrel=EPSREL, epsabs=EPSABS, limit=200)[0]
    I_tau = quad(g_tau, 0.0, math.pi / 2.0, epsrel=EPSREL, epsabs=EPSABS, limit=200)[0]
    I_t = quad(g_t, 0.0, math.pi / 2.0, epsrel=EPSREL, epsabs=EPSABS, limit=200)[0]
    dphi = 2.0 * SQ2 * I_phi
    dtau = (2.0 * SQ2 / L) * I_tau
    dt_c = (2.0 * SQ2 * E / L) * I_t
    return dphi, dt_c, dtau


def cycle_EL(E, L):
    """Exact cycle at invariants (E, L), or None past a type boundary (unbound/plunging)."""
    rr = roots_from_EL(E, L)
    if rr is None:
        return None
    return cycle_from_roots(E, L, *rr)


def cycle_pbar_e(pbar, e):
    E, L, u_p, u_a, u_x = roots_from_pbar_e(pbar, e)
    return cycle_from_roots(E, L, u_p, u_a, u_x) + (E, L)



def derivatives(E, L, C=None):
    """d(dphi,dtau,dt)/d(E,L) by differences of the exact map (the generous version: the
    design stores exact derivatives; nothing real can do better). Steps respect the
    E = 1 (unbound) boundary and shrink if a side leaves the bound domain."""
    if C is None:
        C = cycle_EL(E, L)
    hE = min(1e-5 * max(abs(E), 0.25), 0.2 * (1.0 - E))
    hL = 1e-5 * L

    def col(fn, h):
        for _ in range(6):
            Cp = fn(h)
            Cm = fn(-h)
            if Cp is not None and Cm is not None:
                return [(Cp[i] - Cm[i]) / (2.0 * h) for i in range(3)], None
            if Cp is not None:
                C0_ = cycle_EL(E, L)
                if C0_ is not None:
                    return [(Cp[i] - C0_[i]) / h for i in range(3)], "one-sided+"
            if Cm is not None:
                C0_ = cycle_EL(E, L)
                if C0_ is not None:
                    return [(C0_[i] - Cm[i]) / h for i in range(3)], "one-sided-"
            h *= 0.25
        raise RuntimeError("no derivative stencil at E=%.9g L=%.9g" % (E, L))

    dE, side_e = col(lambda h: cycle_EL(E + h, L), hE)
    dL, side_l = col(lambda h: cycle_EL(E, L + h), hL)
    D = np.zeros((3, 2))
    for i in range(3):
        D[i, 0] = dE[i]
        D[i, 1] = dL[i]
    return D
def chain(E0, L0, kicks, bar_frac=0.10, cap=200000):
    """Kick chain, checkpointed. The state (E, L) is exact at every kick (cumulative sum);
    the description C_hat(n) = C0 + D @ (X_n - X0) is the multiply-add with derivatives
    frozen at the start (the certificate window). The exact map is evaluated only at
    geometric checkpoints (the error is smooth in n); the crossing n* is interpolated in
    (log n, log ratio) between the bracketing checkpoints. Bar: err_dphi > bar_frac * varpi.
    Returns certificate n*, samples (n, err/varpi), and the type event (unbound or plunging).
    """
    kicks = np.asarray(kicks[:cap], dtype=float)
    n_k = len(kicks)
    X0 = np.array([E0, L0])
    Xn = X0[None, :] + np.cumsum(kicks, axis=0)
    C0 = np.array(cycle_EL(E0, L0))
    D = derivatives(E0, L0, tuple(C0))
    Chat = C0[None, :] + (Xn - X0[None, :]) @ D.T  # (n_k, 3) multiply-add description

    # cheap exact type scan: E >= 1 is unbound, no quadrature needed
    i_esc = np.nonzero(Xn[:, 0] >= 1.0)[0]
    n_escape = int(i_esc[0]) + 1 if len(i_esc) else None

    cps = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 16]
    n = 16
    while n < n_k:
        n = int(math.ceil(n * 1.25))
        cps.append(min(n, n_k))
    cps = sorted(set(c for c in cps if c <= n_k))

    samples = []
    n_cross = None
    type_event = None
    last_ratio = None
    for c in cps:
        E_c, L_c = Xn[c - 1]
        C_ex = cycle_EL(E_c, L_c)
        if C_ex is None:
            type_event = {"n": c, "E": float(E_c), "L": float(L_c),
                          "hat_dphi": float(Chat[c - 1, 0]), "hat_dt": float(Chat[c - 1, 1]),
                          "kind": "plunging/marginal between checkpoints",
                          "note": "no bound cycle exists at this state; the multiply-add "
                                  "still returns one (type blindness)"}
            if n_cross is None:
                n_cross = c  # conservative: the bar may break even earlier
            break
        varpi = C_ex[0] - 2.0 * math.pi
        if varpi <= 0.0:
            varpi = 1e-300
        ratio = abs(Chat[c - 1, 0] - C_ex[0]) / varpi
        samples.append((c, float(ratio)))
        if n_cross is None and ratio > bar_frac:
            if last_ratio is not None and last_ratio > 0:
                # interpolate in (log n, log ratio)
                c_prev, r_prev = samples[-2]
                frac = (math.log(bar_frac) - math.log(r_prev)) / (math.log(ratio) - math.log(r_prev))
                n_cross = c_prev * (c / c_prev) ** frac
            else:
                n_cross = c
        last_ratio = ratio
    if n_escape is not None and (type_event is None or n_escape <= type_event["n"]):
        type_event = {"n": n_escape, "E": float(Xn[n_escape - 1, 0]),
                      "L": float(Xn[n_escape - 1, 1]),
                      "hat_dphi": float(Chat[n_escape - 1, 0]),
                      "hat_dt": float(Chat[n_escape - 1, 1]),
                      "kind": "unbound (E>=1)",
                      "note": "the orbit escaped; the multiply-add still returns a cycle"}
    return {"n_cert": (float(n_cross) if n_cross is not None else None),
            "n_run": int(cps[-1] if cps else 0), "samples": samples,
            "type_event": type_event, "final_E": float(Xn[-1, 0]), "final_L": float(Xn[-1, 1])}
def extrapolate(samples, bar_frac=0.10):
    """Fit log(err/varpi) = a + b log(n) on the second half of the samples; extrapolate to the
    bar. Returns (N*, b, r2) or None."""
    s = [(n, r) for n, r in samples if r > 1e-16]
    if len(s) < 8:
        return None
    half = s[len(s) // 2:]
    x = np.log([n for n, _ in half])
    y = np.log([r for _, r in half])
    b, a = np.polyfit(x, y, 1)
    yh = a + b * x
    ss_res = float(np.sum((y - yh) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    if b <= 0:
        return None
    n_star = math.exp((math.log(bar_frac) - a) / b)
    return n_star, float(b), r2


def validate():
    """Instrument controls: 6 pi / pbar convergence, the Kepler dt limit, and an independent
    Binet-ODE integration of dphi at a strong and a mild point."""
    out = []
    for pbar in (1e4, 1e5, 1e6):
        for e in (0.2, 0.6):
            dphi, dt_c, dtau, E, L = cycle_pbar_e(pbar, e)
            varpi = dphi - 2.0 * math.pi
            lead = 6.0 * math.pi / pbar
            out.append({"pbar": pbar, "e": e, "varpi": varpi, "6pi_over_pbar": lead,
                        "ratio": varpi / lead})
    kepler = []
    for pbar in (1e4, 1e5):
        for e in (0.2, 0.6):
            dphi, dt_c, dtau, E, L = cycle_pbar_e(pbar, e)
            a = pbar / (1.0 - e * e)
            kepler.append({"pbar": pbar, "e": e, "dt": dt_c,
                           "kepler_dt": 2.0 * math.pi * a ** 1.5,
                           "rel": dt_c / (2.0 * math.pi * a ** 1.5) - 1.0})
    # independent check: integrate the Binet equation u'' + u = 1/L^2 + 3 u^2 (M = 1)
    # from pericentre through the next pericentre.
    from scipy.integrate import solve_ivp
    binet = []
    for pbar, e in ((20.0, 0.5), (1000.0, 0.6)):
        E0, L0, u_p, u_a, u_x = roots_from_pbar_e(pbar, e)

        def rhs(phi, y):
            return (y[1], 1.0 / (L0 * L0) + 3.0 * y[0] * y[0] - y[0])

        def up_up(phi, y):
            return y[1]
        up_up.terminal = True
        up_up.direction = 1.0  # fires where u' crosses 0 upward: apocentre (not at the start)
        s1 = solve_ivp(rhs, (0.0, 1e6), (u_p, 0.0), rtol=1e-13, atol=1e-15,
                       events=up_up, dense_output=False)
        phi_apo = s1.t_events[0][0]
        u_apo = s1.y_events[0][0][0]

        def down_down(phi, y):
            return y[1]
        down_down.terminal = True
        down_down.direction = -1.0  # fires where u' crosses 0 downward: the next pericentre
        s2 = solve_ivp(rhs, (phi_apo, 1e6), (u_apo, 0.0), rtol=1e-13, atol=1e-15,
                       events=down_down, dense_output=False)
        phi_peri2 = s2.t_events[0][0]
        dphi_q, _, _, _, _ = cycle_pbar_e(pbar, e)
        binet.append({"pbar": pbar, "e": e, "dphi_quadrature": dphi_q,
                      "dphi_binet_ode": phi_peri2,
                      "rel": phi_peri2 / dphi_q - 1.0})
    return {"precession": out, "kepler": kepler, "binet": binet}


def main():
    mode = "grid"
    if len(__import__("sys").argv) > 1:
        mode = __import__("sys").argv[1]
    if mode == "validate":
        print(json.dumps(validate(), indent=1))
        return
    rng = np.random.default_rng(20261021)
    results = {"validate": validate()}
    grid = []
    bar_frac = 0.10
    cells = [
        ("belt-like", 1e5, 0.2),
        ("belt-tail", 1e4, 0.6),
        ("r3-heartland", 1000.0, 0.6),
        ("license-edge", 65.0, 0.6),
        ("strong", 20.0, 0.5),
        ("whirl", 16.0, 0.99),
        ("near-sep", 16.05, 0.99),  # p_peri = 8.066, separatrix at 6+2e = 7.98: margin 0.086
    ]
    for name, pbar, e in cells:
        dphi0, dt0, dtau0, E0, L0 = cycle_pbar_e(pbar, e)
        bind = 1.0 - E0  # binding scale: tidal kicks are fractional in THIS, not in E ~ 1
        for delta in (1e-6, 1e-4, 1e-2):
            for prog in ("random", "coherent-dL", "coherent-dE"):
                if prog == "random":
                    kicks = [(delta * bind * rng.standard_normal(), delta * L0 * rng.standard_normal())
                             for _ in range(200000)]
                elif prog == "coherent-dL":
                    kicks = [(0.0, -delta * L0)] * 200000
                else:
                    kicks = [(delta * bind, 0.0)] * 200000  # dE>0: toward escape
                ch = chain(E0, L0, kicks, bar_frac=bar_frac, cap=200000)
                ex = extrapolate(ch["samples"], bar_frac)
                grid.append({
                    "cell": name, "pbar": pbar, "e": e, "delta": delta, "program": prog,
                    "dphi0": dphi0, "varpi0": dphi0 - 2 * math.pi,
                    "n_cert_measured": ch["n_cert"], "n_run": ch["n_run"],
                    "err_frac_last": ch["samples"][-1][1] if ch["samples"] else None,
                    "n_cert_extrapolated": (None if ex is None else ex[0]),
                    "growth_b": (None if ex is None else ex[1]),
                    "fit_r2": (None if ex is None else ex[2]),
                    "type_event": ch["type_event"],
                })
    results["grid"] = grid

    # ---- the type arm: a kick that crosses the separatrix (plunge) -----------------
    pbar, e = 16.05, 0.99
    dphi0, dt0, dtau0, E0, L0 = cycle_pbar_e(pbar, e)
    sep = 6.0 + 2.0 * e
    p_peri0 = pbar / (1.0 + e)
    kicks = [(0.0, -1e-2 * L0)] * 2000
    ch = chain(E0, L0, kicks, bar_frac=bar_frac, cap=2000)
    results["type_arm"] = {"pbar": pbar, "e": e, "p_peri0": p_peri0, "separatrix": sep,
                           "margin_M": p_peri0 - sep, "chain": ch}

    with open("grid.json", "w") as f:
        json.dump(results, f, indent=1)
    # console digest
    for row in grid:
        print("%-13s pbar=%-8g e=%-5g d=%-7g %-12s N*=%s (extr %s, b=%s) type=%s" % (
            row["cell"], row["pbar"], row["e"], row["delta"], row["program"],
            row["n_cert_measured"], row["n_cert_extrapolated"], row["growth_b"],
            bool(row["type_event"])))
    print(json.dumps(results["type_arm"], indent=1)[:1500])


if __name__ == "__main__":
    main()
