#!/usr/bin/env python3
"""Red-team probe: premise 3 of docs/representation.md.

"A cycle's derivatives are stored with it, so a kick updates the cycle by a
multiply-add" (the jet). Oracle: float64 Schwarzschild timelike geodesics,
Binet ODE u'' + u = 1/L^2 + 3u^2 (M=1), RK4 in the angle phi; per radial
cycle we measure dphi (periapsis-to-periapsis angle) and T (coordinate period
via dt/dphi = E/(L u^2 (1-2u)), Simpson). Jet = first-order Taylor of
(dphi, T) in (E, L). Floor 1e-6 relative (df81's floor).

Cases: belt-like (p, e) grid; correlated-kick walks at several quantum sizes
alpha (recompile interval N ~ 1/alpha, error ~ N^2); plunge-separatrix
approach at fixed L = L_s (unstable circular at r_c = 5M).
"""
import json
import math

FLOOR = 1e-6


def roots_R(E, L):
    """Real roots of R(u) = E^2 - (1-2u)(1+L^2 u^2), ascending."""
    import numpy as np
    a, b, c, d = 2 * L * L, -L * L, 2.0, E * E - 1.0
    r = np.roots([a, b, c, d])
    return sorted(float(np.real(x)) for x in r if abs(np.imag(x)) < 1e-9)


def orbit(E, L, h=1e-3, cap_phi=200.0):
    """One radial cycle from periapsis. Returns (dphi, T), or None if plunge."""
    rs = roots_R(E, L)
    if len(rs) < 3:
        return None
    u_apo, u_per, u_hor = rs[0], rs[1], rs[2]  # bound band u in [u_apo, u_per]
    if u_apo <= 0.0 or u_per >= 0.5 - 1e-9:
        return None  # inner turning point gone: plunge
    u0 = u_per
    def f(u):
        return 1.0 / (L * L) + 3.0 * u * u - u
    def g(u):
        return E / (L * u * u * (1.0 - 2.0 * u))
    u, up, up_prev, phi = u0, 0.0, 0.0, 0.0
    passed_apo = False
    gs = [g(u)]
    while phi < cap_phi:
        k1u, k1v = up, f(u)
        k2u, k2v = up + 0.5 * h * k1v, f(u + 0.5 * h * k1u)
        k3u, k3v = up + 0.5 * h * k2v, f(u + 0.5 * h * k2u)
        k4u, k4v = up + h * k3v, f(u + h * k3u)
        u_new = u + (h / 6.0) * (k1u + 2 * k2u + 2 * k3u + k4u)
        up_new = up + (h / 6.0) * (k1v + 2 * k2v + 2 * k3v + k4v)
        phi_new = phi + h
        if up_prev < 0.0 <= up_new:
            passed_apo = True
        gs.append(0.5 * (g(u) + g(u_new)))
        u, up_prev, phi = u_new, up, phi_new
        up = up_new
        if passed_apo and up_prev > 0.0 >= up:
            # periapsis return (u maximum): up is locally linear in phi
            x = up_prev * h / (up_prev - up)  # forward distance from phi-h
            phi_p = phi - h + x
            break
    else:
        return None  # cycle longer than cap (deep whirl): excluded
    if len(gs) % 2 == 0:
        gs = gs[:-1]
    T = (h / 3.0) * (gs[0] + gs[-1] + 4 * sum(gs[1:-1:2]) + 2 * sum(gs[2:-1:2]))
    T += g(u) * (phi_p - (len(gs) - 1) * h)
    return (phi_p, T)

def cycle(E, L, **kw):
    return orbit(E, L, **kw)


def derivatives(E, L, dh_rel=1e-7):
    """(dphi_E, T_E, dphi_L, T_L) by central differences; None if any probe plunges."""
    dE, dL = dh_rel * abs(E), dh_rel * L
    pP, pM = cycle(E + dE, L), cycle(E - dE, L)
    qP, qM = cycle(E, L + dL), cycle(E, L - dL)
    if None in (pP, pM, qP, qM):
        return None
    return ((pP[0] - pM[0]) / (2 * dE), (pP[1] - pM[1]) / (2 * dE),
            (qP[0] - qM[0]) / (2 * dL), (qP[1] - qM[1]) / (2 * dL))


def jet_err(E, L, kick_E=0.0, kick_L=0.0):
    """Relative error of the one-kick jet on (dphi, T); strings for degenerate cases."""
    base = cycle(E, L)
    if base is None:
        return "base-plunge"
    der = derivatives(E, L)
    if der is None:
        return "div"
    new = cycle(E + kick_E, L + kick_L)
    if new is None:
        return "plunge-after-kick"
    jd = base[0] + der[0] * kick_E + der[2] * kick_L
    jT = base[1] + der[1] * kick_E + der[3] * kick_L
    return max(abs(jd - new[0]) / new[0], abs(jT - new[1]) / new[1])


def EL_from_pe(p, e):
    ua, up = (1 - e) / p, (1 + e) / p  # u at apoapsis, periapsis
    L2 = 2 * (ua - up) / ((1 - 2 * ua) * ua * ua - (1 - 2 * up) * up * up)
    E2 = (1 - 2 * up) * (1 + L2 * up * up)
    return math.sqrt(E2), math.sqrt(L2)


def walk_jet(E, L, alpha, nmax=300000):
    """Correlated quantum kicks (alpha relative on E and L, same sign).
    Jet holds the base cycle's stored derivatives (the mechanism). Returns
    list of (N, jet_err) sampled geometrically, plus plunge N if any."""
    base = cycle(E, L)
    der = derivatives(E, L)
    dE, dL = alpha * abs(E), alpha * L
    pts, plunge_N = [], None
    Ns = sorted(set(min(nmax, max(1, int(round(10 ** (k / 4.0))))) for k in range(0, 29)))
    for N in Ns:
        cur = cycle(E + N * dE, L + N * dL)
        if cur is None:
            plunge_N = N
            break
        jd = base[0] + der[0] * (N * dE) + der[2] * (N * dL)
        jT = base[1] + der[1] * (N * dE) + der[3] * (N * dL)
        err = max(abs(jd - cur[0]) / cur[0], abs(jT - cur[1]) / cur[1])
        pts.append((N, err))
        if err > 1e-3:
            break
    return pts, plunge_N


def main():
    out = {}

    # oracle self-check: weak-field precession 6pi/p
    E, L = EL_from_pe(100.0, 0.5)
    r = cycle(E, L)
    # convergence check on one case
    r2 = cycle(E, L, h=5e-4)
    out["oracle_check"] = {
        "p": 100, "e": 0.5,
        "dphi_minus_2pi": r[0] - 2 * math.pi,
        "6pi_over_p": 6 * math.pi / 100,
        "T_h_refine_rel": abs(r2[1] - r[1]) / r[1],
        "dphi_h_refine_rel": abs(r2[0] - r[0]) / r[0],
    }

    # P1: single quantum kick (alpha=1e-6 on E, and on L), belt-like domain
    p1 = []
    for p in (20.0, 100.0):
        for e in (0.1, 0.5, 0.7, 0.9, 0.99):
            E, L = EL_from_pe(p, e)
            p1.append({"p": p, "e": e, "r_apo": p / (1 - e),
                       "jet_err_kickE": jet_err(E, L, kick_E=1e-6 * E),
                       "jet_err_kickL": jet_err(E, L, kick_L=1e-6 * L)})
    out["P1_single_quantum_kick"] = p1
    out["P4_e_sweep_p20"] = [
        {"e": row["e"], "max_err": max(row["jet_err_kickE"], row["jet_err_kickL"])}
        for row in p1 if row["p"] == 20.0]

    # P2: walks from belt base p=20, e=0.5
    E0, L0 = EL_from_pe(20.0, 0.5)
    p2 = []
    for alpha in (1e-7, 1e-6, 1e-5):
        pts, plunge_N = walk_jet(E0, L0, alpha)
        n_floor = next((N for N, err in pts if err > FLOOR), None)
        # local exponent of err vs N (should be ~2)
        exp = None
        if len(pts) >= 4 and pts[-1][1] > 0:
            import math as m
            x0, x1 = pts[-4], pts[-1]
            if x0[1] > 0 and x1[0] > x0[0]:
                exp = m.log(x1[1] / x0[1]) / m.log(x1[0] / x0[0])
        p2.append({"alpha": alpha, "N_floor": n_floor, "plunge_N": plunge_N,
                   "exponent_err_vs_N": exp,
                   "last": pts[-1] if pts else None})
    out["P2_walks"] = p2

    # P3: separatrix at r_c = 5M: L_s^2 = 25/2, E_s^2 = 9/10
    Ls, Es = math.sqrt(25 / 2), math.sqrt(9 / 10)
    p3 = []
    for eps in [10 ** -k for k in range(2, 7)]:
        E = Es * (1 - eps)
        c = cycle(E, Ls)
        der = derivatives(E, Ls)
        p3.append({
            "eps": eps, "dphi": c[0] if c else None, "T": c[1] if c else None,
            "jet_err_kickE_1e-6": (jet_err(E, Ls, kick_E=1e-6 * E) if c and der else None),
            "jet_err_kickL_1e-6": (jet_err(E, Ls, kick_L=1e-6 * Ls) if c and der else None),
            "abs_dT_dE": abs(der[1]) if der else None,
        })
    out["P3_separatrix"] = p3

    # P3b: kick-size band at eps=1e-3 from separatrix (encounter-grade kicks)
    E = Es * (1 - 1e-3)
    out["P3b_kick_size_band"] = [
        {"alpha": a,
         "kickE": jet_err(E, Ls, kick_E=a * abs(E)),
         "kickL": jet_err(E, Ls, kick_L=a * Ls)}
        for a in (1e-6, 1e-5, 1e-4, 1e-3, 3e-3, 1e-2)]

    # P3c: r1's ISCO seed, corrected to a physical tangential launch at r=7:
    # L = 1.01 L_circ(7); E^2 = (1-2/r0)(1+L^2/r0^2); E_sep from the unstable
    # circular branch r_c in (4,6): r_c^2 - L^2 r_c + 3L^2 = 0
    Lc7 = math.sqrt(49 / 4)
    L = 1.01 * Lc7
    E = math.sqrt((1 - 2 / 7.0) * (1 + L * L / 49.0))
    L2 = L * L
    rc = 0.5 * (L2 - math.sqrt(L2 * L2 - 12 * L2))
    Esep = math.sqrt((1 - 2 / rc) * (1 + L2 / (rc * rc)))
    seed = {
        "E": E, "L": L, "birth_cycle": cycle(E, L),
        "r_c_unstable": rc, "E_sep_for_this_L": Esep,
        "E_sep_gap_rel": (Esep - E) / E,
        "L_seed_over_Ls_rc5": L / Ls,
        "jet_err_kickE_1e-6_at_seed": jet_err(E, L, kick_E=1e-6 * E),
        "jet_err_kickE_1e-3_at_eps1e-3": jet_err(Esep * (1 - 1e-3), L,
                                                 kick_E=1e-3 * Esep),
        "jet_err_kickE_1e-6_at_eps1e-3": jet_err(Esep * (1 - 1e-3), L,
                                                 kick_E=1e-6 * Esep),
    }
    out["P3c_r1_isco_seed"] = seed

    with open("probe_out.json", "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
