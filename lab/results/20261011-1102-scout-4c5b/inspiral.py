#!/usr/bin/env python3
"""Inspiral generator falsifier — scout run 20261011-1102-scout-4c5b.

M = G = c = 1 throughout. The binary is one doll of total mass M=1, reduced mass
nu = m1*m2 (since M=1). The relative orbit is the exact Schwarzschild tube with
per-unit-reduced-mass invariants (E, L). Radiation reaction = orbit-averaged
quadrupole flux balance (Peters) evaluated on the EXACT orbit (a, e) read from
the cubic's turning points:
    R(u) = 2 L^2 u^3 - L^2 u^2 + 2 u + (E^2 - 1),   u = 1/r
Bound iff three distinct positive real roots u_a < u_p < u_3 (u_a apocenter).
Vieta: u_a + u_p + u_3 = 1/2  (independent of E, L).
Circular family (exact): E^2 = (1-2/r)^2/(1-3/r), L^2 = r/(r-3), ISCO at r=6.

Parts:
  W1: numerical quadrupole-formula average over a Newtonian ellipse vs the
      Peters-Mathews closed form f(e).  (independent derivation of the flux;
      exact eta-space evaluation: the orbit is a trig polynomial in the
      eccentric anomaly, time derivatives by the chain rule through
      dt/deta = w = 1 - e cos(eta); the period average carries the weight w.)
  W2: circular generator vs Peters' closed form a(t) = a0 (1-t/tc)^{1/4}.
  M : the generator on the exact tube: separatrix handoff, re-key walls at
      eps_bar in {1e-2, 1e-3}, orbits inside the wall, spurious eccentricity.
  PN: merger-time deficit decomposition (geometry vs flux) at 1PN(+tail).
Outputs: inspiral-out.json, summary printed.
"""
import json
import numpy as np

# ----------------------------------------------------------------- fluxes ---
def peters_F(e):
    """F~(e) = (1+73 e^2/24 + 37 e^4/96)/(1-e^2)^{7/2}."""
    e2 = e * e
    return (1.0 + 73.0 / 24.0 * e2 + 37.0 / 96.0 * e2 * e2) / (1.0 - e2) ** 3.5

def flux_L(a, e, nu, pn=False):
    """GW luminosity. Newtonian quadrupole; optional 1PN+tail circular
    correction (Blanchet 2014): 1 - (1247/336 + 35 nu/12)/a + 4 pi/a^{3/2}."""
    base = (32.0 / 5.0) * nu * nu * peters_F(e) / a**5
    if pn:
        if e > 1e-9:
            raise ValueError("1PN amplitude implemented for circular only")
        base *= 1.0 - (1247.0 / 336.0 + 35.0 * nu / 12.0) / a + 4.0 * np.pi / a**1.5
    return base

def flux_G(a, e, nu):
    """Angular-momentum flux (Peters)."""
    e2 = e * e
    return (32.0 / 5.0) * nu * nu * (1.0 + 7.0 / 8.0 * e2) / (a**3.5 * (1.0 - e2) ** 2)

# ------------------------------------------------------- the exact tube -----
def roots_exact(E, L):
    """All real roots of R, sorted; None if not three distinct positive."""
    c = np.array([2.0 * L * L, -L * L, 2.0, E * E - 1.0])
    r = np.roots(c)
    if np.max(np.abs(r.imag)) > 1e-9:
        return None
    u = np.sort(r.real)
    if u[0] <= 0.0:
        return None
    if not (u[1] - u[0] > 1e-9 * u[1] and u[2] - u[1] > 1e-9 * u[1]):
        return None
    return u

def roots_newton(E, L, ua, up):
    """Refine (ua, up) by Newton from previous values; u3 by Vieta."""
    A, B, C, D = 2.0 * L * L, -L * L, 2.0, E * E - 1.0
    for _ in range(80):
        for which in (0, 1):
            u = ua if which == 0 else up
            Rv = ((A * u + B) * u + C) * u + D
            dR = (3.0 * A * u + 2.0 * B) * u + C
            if which == 0:
                ua = u - Rv / dR
            else:
                up = u - Rv / dR
        Rv_a = ((A * ua + B) * ua + C) * ua + D
        Rv_p = ((A * up + B) * up + C) * up + D
        if max(abs(Rv_a), abs(Rv_p)) < 1e-13:
            break
    u3 = 0.5 - ua - up
    ok = 0.0 < ua < up < u3
    return ua, up, u3, ok

def ae_from_u(ua, up):
    ra, rp = 1.0 / ua, 1.0 / up
    return 0.5 * (ra + rp), (ra - rp) / (ra + rp)

def EL_from_ae(a0, e0):
    """Exact (E, L) whose turning points are r_p = a0(1-e0), r_a = a0(1+e0)."""
    ua, up = 1.0 / (a0 * (1.0 + e0)), 1.0 / (a0 * (1.0 - e0))
    u3 = 0.5 - ua - up
    L2 = 1.0 / (ua * up + ua * u3 + up * u3)
    E2 = 1.0 - 2.0 * L2 * ua * up * u3
    return np.sqrt(max(E2, 0.0)), np.sqrt(max(L2, 0.0))

# ------------------------------------------------- exact circular family ----
E_ISCO = np.sqrt(8.0 / 9.0)

def circ_r(E):
    if E <= E_ISCO:
        return 6.0
    E2 = E * E
    disc = E * np.sqrt(9.0 * E2 - 8.0)
    return (3.0 * E2 - 4.0 - disc) / (2.0 * (E2 - 1.0))

def circ_E(a):
    return np.sqrt((1.0 - 2.0 / a) ** 2 / (1.0 - 3.0 / a))

def circ_L(a):
    return np.sqrt(a / (a - 3.0))

def circ_dEda(a):
    h = 1e-5 * a
    return (circ_E(a + h) - circ_E(a - h)) / (2.0 * h)

# ------------------------------------------------------------------- W1 -----
def w1_quadrupole():
    """(1/5)<q''' q'''> over a Newtonian ellipse (mu=1, a=1) vs (32/5) f(e).
      d/dt f   = f'/w
      d2/dt2 f = f''/w^2 - f' w'/w^3
      d3/dt3 f = f'''/w^3 - 3 f'' w'/w^4 - f' w''/w^4 + 3 f' w'^2/w^5
    """
    out = []
    for e in [0.0, 0.1, 0.3, 0.5, 0.7, 0.9]:
        n = 1 << 10
        eta = 2.0 * np.pi * np.arange(n) / n
        b = np.sqrt(1.0 - e * e)
        x, y = np.cos(eta) - e, b * np.sin(eta)
        x1, x2, x3 = -np.sin(eta), -np.cos(eta), np.sin(eta)
        y1, y2, y3 = b * np.cos(eta), -b * np.sin(eta), -b * np.cos(eta)
        w, w1, w2 = 1.0 - e * np.cos(eta), e * np.sin(eta), e * np.cos(eta)

        def d3t(f1, f2, f3):
            return (f3 / w**3 - 3.0 * f2 * w1 / w**4
                    - f1 * w2 / w**4 + 3.0 * f1 * w1 * w1 / w**5)

        g = {
            "xx": (x * x, 2 * x * x1, 2 * (x1 * x1 + x * x2),
                   6 * x1 * x2 + 2 * x * x3),
            "yy": (y * y, 2 * y * y1, 2 * (y1 * y1 + y * y2),
                   6 * y1 * y2 + 2 * y * y3),
            "xy": (x * y, x1 * y + x * y1,
                   x2 * y + 2 * x1 * y1 + x * y2,
                   x3 * y + 3 * x2 * y1 + 3 * x1 * y2 + x * y3),
        }
        dxx = (2.0 / 3.0) * d3t(*g["xx"][1:]) - (1.0 / 3.0) * d3t(*g["yy"][1:])
        dyy = (2.0 / 3.0) * d3t(*g["yy"][1:]) - (1.0 / 3.0) * d3t(*g["xx"][1:])
        dxy = d3t(*g["xy"][1:])
        dzz = -(d3t(*g["xx"][1:]) + d3t(*g["yy"][1:])) / 3.0   # Q_zz = -r^2/3
        integrand = (dxx * dxx + dyy * dyy + dzz * dzz + 2.0 * dxy * dxy) * w
        P = np.mean(integrand) / 5.0
        P_closed = (32.0 / 5.0) * peters_F(e)
        out.append({"e": e, "numeric": P, "closed": P_closed,
                    "relerr": abs(P / P_closed - 1.0)})
    return out

# ------------------------------------------------------------------- W2 -----
def w2_circular_wiring(nu=0.25, a0=100.0):
    dadt = lambda a: -(64.0 / 5.0) * nu / a**3
    a, t = a0, 0.0
    while a > 6.0:
        P = 2.0 * np.pi * a**1.5
        dt = P / 64.0
        k1 = dadt(a); k2 = dadt(a + .5 * dt * k1)
        k3 = dadt(a + .5 * dt * k2); k4 = dadt(a + dt * k3)
        a += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        t += dt
    t_true = (5.0 / (256.0 * nu)) * (a0**4 - 6.0**4)
    return {"t_num": t, "t_closed": t_true, "relerr": abs(t / t_true - 1.0)}

# ------------------------------------------------------------ generators ----
def run_eccentric(nu, a0, e0, eps_bars=(1e-2, 1e-3)):
    """(E, L) drift by both Peters fluxes on the exact orbit."""
    E, L = EL_from_ae(a0, e0)
    u = roots_exact(E, L)
    assert u is not None, "bad initial orbit"
    ua, up, u3 = u[0], u[1], u[2]
    n_orb = 0.0
    rekeys = {eb: 0 for eb in eps_bars}
    pend = {eb: 0.0 for eb in eps_bars}
    walls, wall_orbit = {}, {}
    for eb in eps_bars:
        walls[eb] = None
        wall_orbit[eb] = None
    max_e = 0.0
    a_end = e_end = None
    last_good = [None, None]

    def fluxes(E_, L_, ua_, up_):
        ua2, up2, u32, ok = roots_newton(E_, L_, ua_, up_)
        if not ok:
            u_ = roots_exact(E_, L_)
            if u_ is None:
                return None
            ua2, up2, u32 = u_
        a_, e_ = ae_from_u(ua2, up2)
        return (-flux_L(a_, e_, nu) / nu, -flux_G(a_, e_, nu) / nu,
                ua2, up2, u32, a_, e_)

    while True:
        f = fluxes(E, L, ua, up)
        if f is None:
            break
        dEdt, dLdt, ua, up, u3, a, e = f
        if u3 - up < 1e-6 * up:          # separatrix: bound pair merges
            a_end, e_end = a, e
            break
        last_good = [a, e]
        max_e = max(max_e, e)
        P = 2.0 * np.pi * a**1.5
        da_orb = (64.0 / 5.0) * nu * peters_F(e) / a**3 * P
        dlnP = 1.5 * abs(da_orb) / a
        for eb in eps_bars:
            if walls[eb] is None and dlnP >= eb:
                walls[eb] = a
                wall_orbit[eb] = n_orb
        dt = P * min(0.5, 0.05 / max(dlnP, 1e-15))
        # RK4 with dt-halving when a trial stage leaves the bound region
        for _ in range(40):
            k1 = fluxes(E, L, ua, up)
            k2 = (None if k1 is None else
                  fluxes(E + .5 * dt * k1[0], L + .5 * dt * k1[1], k1[2], k1[3]))
            k3 = (None if k2 is None else
                  fluxes(E + .5 * dt * k2[0], L + .5 * dt * k2[1], k2[2], k2[3]))
            k4 = (None if k3 is None else
                  fluxes(E + dt * k3[0], L + dt * k3[1], k3[2], k3[3]))
            if None not in (k1, k2, k3, k4):
                break
            dt *= 0.5
        else:
            a_end, e_end = last_good     # cannot step: handoff here
            break
        if None in (k1, k2, k3, k4):
            a_end, e_end = last_good
            break
        E += dt * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6.0
        L += dt * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6.0
        ua, up = k4[2], k4[3]
        n_orb += dt / P
        for eb in eps_bars:
            pend[eb] += dlnP * dt / P
            while pend[eb] >= eb:
                pend[eb] -= eb
                rekeys[eb] += 1
    if a_end is None:
        u_ = roots_exact(E, L)
        if u_ is not None:
            a_end, e_end = ae_from_u(u_[0], u_[1])
        else:
            a_end, e_end = last_good     # stepped past the separatrix
    inside = {f"{eb:g}": (n_orb - wall_orbit[eb]) if wall_orbit[eb] is not None
              else None for eb in eps_bars}
    return {"nu": nu, "a0": a0, "e0": e0, "orbits": n_orb,
            "a_end": a_end, "e_end": e_end, "max_e": max_e,
            "walls": {f"{eb:g}": walls[eb] for eb in eps_bars},
            "orbits_inside_wall": inside,
            "rekeys_strong": {f"{eb:g}": rekeys[eb] for eb in eps_bars}}

def run_circular(nu, a0, eps_bars=(1e-2, 1e-3), pn=False, spurious_e=False):
    """Circular: state E; L = L(E) (geometry projection), or two-flux drift
    (spurious_e) measuring the induced eccentricity."""
    E = circ_E(a0)
    L = circ_L(a0)
    n_orb, t = 0.0, 0.0
    rekeys = {eb: 0 for eb in eps_bars}
    pend = {eb: 0.0 for eb in eps_bars}
    walls, wall_orbit = {}, {}
    for eb in eps_bars:
        walls[eb] = None
        wall_orbit[eb] = None
    max_e = 0.0
    while E > E_ISCO + 1e-13:
        a = circ_r(E)
        P = 2.0 * np.pi * a**1.5
        dEdt = lambda E_: -flux_L(circ_r(E_), 0.0, nu, pn=pn) / nu
        da_orb = abs(dEdt(E)) * P / abs(circ_dEda(a))
        dlnP = 1.5 * da_orb / a
        for eb in eps_bars:
            if walls[eb] is None and dlnP >= eb:
                walls[eb] = a
                wall_orbit[eb] = n_orb
        dt = P * min(0.25, 0.02 / max(dlnP, 1e-15))
        k1 = dEdt(E)
        k2 = dEdt(E + .5 * dt * k1)
        k3 = dEdt(E + .5 * dt * k2)
        k4 = dEdt(E + dt * k3)
        E = E + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        if spurious_e:
            L += -flux_G(a, 0.0, nu) / nu * dt
            u_ = roots_exact(E, L)
            if u_ is not None:
                max_e = max(max_e, ae_from_u(u_[0], u_[1])[1])
        else:
            L = circ_L(circ_r(E))
        n_orb += dt / P
        t += dt
        for eb in eps_bars:
            pend[eb] += dlnP * dt / P
            while pend[eb] >= eb:
                pend[eb] -= eb
                rekeys[eb] += 1
    inside = {f"{eb:g}": (n_orb - wall_orbit[eb]) if wall_orbit[eb] is not None
              else None for eb in eps_bars}
    return {"nu": nu, "a0": a0, "orbits": n_orb, "t_merge": t,
            "a_end": 6.0, "walls": {f"{eb:g}": walls[eb] for eb in eps_bars},
            "orbits_inside_wall": inside,
            "rekeys_strong": {f"{eb:g}": rekeys[eb] for eb in eps_bars},
            "max_e": max_e}

# ------------------------------------------------------------------- PN -----
def t_merge_newtonian_closed(nu, a0, a_end=6.0):
    return (5.0 / (256.0 * nu)) * (a0**4 - a_end**4)

def t_merge_newtonian_ode(nu, a0, a_end=6.0, pn=False):
    a, t = a0, 0.0
    while a > a_end:
        P = 2.0 * np.pi * a**1.5
        dt = P / 8.0

        def k(x):
            corr = (1.0 - (1247.0 / 336.0 + 35.0 * nu / 12.0) / x
                    + 4.0 * np.pi / x**1.5) if pn else 1.0
            return -(64.0 / 5.0) * nu / x**3 * corr

        k1 = k(a); k2 = k(a + .5 * dt * k1)
        k3 = k(a + .5 * dt * k2); k4 = k(a + dt * k3)
        a += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        t += dt
    return t

def pn_block(nu=0.25):
    out = []
    for a0 in [20.0, 100.0, 600.0]:
        tN = t_merge_newtonian_closed(nu, a0)
        tN_ode = t_merge_newtonian_ode(nu, a0)
        t_flux = t_merge_newtonian_ode(nu, a0, pn=True)
        t_geo = run_circular(nu, a0, eps_bars=())["t_merge"]
        t_both = run_circular(nu, a0, eps_bars=(), pn=True)["t_merge"]
        out.append({"a0": a0, "t_newton_closed": tN, "t_newton_ode": tN_ode,
                    "t_flux1pn_newtonfam": t_flux,
                    "t_newtonflux_exactfam": t_geo,
                    "t_1pnflux_exactfam": t_both,
                    "flux_deficit_pct": 100 * (t_flux / tN - 1.0),
                    "geometry_pct": 100 * (t_geo / tN - 1.0),
                    "both_pct": 100 * (t_both / tN - 1.0)})
    return out

# ------------------------------------------------------------------ main ----
if __name__ == "__main__":
    res = {}
    print("== W1 quadrupole average vs Peters-Mathews ==")
    res["W1"] = w1_quadrupole()
    for r in res["W1"]:
        print(f"  e={r['e']:.1f}  relerr = {r['relerr']:.2e}")

    print("== W2 circular wiring ==")
    res["W2"] = w2_circular_wiring()
    print(f"  t_num/t_closed relerr = {res['W2']['relerr']:.2e}")

    print("== M: generator on the exact tube (eccentric) ==")
    res["M_ecc"] = []
    for nu, a0 in [(0.25, 100.0), (0.01, 100.0), (1e-3, 30.0)]:
        for e0 in [0.3, 0.6, 0.9]:
            r = run_eccentric(nu, a0, e0)
            tot = {}
            for eb in (1e-2, 1e-3):
                aw = r["walls"][f"{eb:g}"]
                tot[f"{eb:g}"] = (1.5 * np.log(1000.0 / aw) / eb
                                  if (aw is not None and aw < 1000.0) else 0.0)
            r["rekeys_from_1000"] = tot
            res["M_ecc"].append(r)
            print(f"  nu={nu:g} e0={e0} a0={a0:.0f}: orbits={r['orbits']:.0f} "
                  f"a_end={r['a_end'] and round(r['a_end'],1)} "
                  f"e_end={r['e_end'] and round(r['e_end'],3)} "
                  f"w1e-2={r['walls']['0.01'] and round(r['walls']['0.01'],1)} "
                  f"w1e-3={r['walls']['0.001'] and round(r['walls']['0.001'],1)} "
                  f"inside(w1e-2)={r['orbits_inside_wall']['0.01'] and round(r['orbits_inside_wall']['0.01'])} "
                  f"max_e={r['max_e']:.4f}")

    print("== M: circular (exact family) ==")
    res["M_circ"] = []
    for nu, a0 in [(0.25, 100.0), (0.01, 100.0), (1e-3, 30.0)]:
        r = run_circular(nu, a0)
        res["M_circ"].append(r)
        print(f"  nu={nu:g} a0={a0:.0f}: orbits={r['orbits']:.0f} a_end={r['a_end']:.2f} "
              f"w1e-2={r['walls']['0.01'] and round(r['walls']['0.01'],1)} "
              f"w1e-3={r['walls']['0.001'] and round(r['walls']['0.001'],1)} "
              f"inside(w1e-2)={r['orbits_inside_wall']['0.01'] and round(r['orbits_inside_wall']['0.01'])} "
              f"inside(w1e-3)={r['orbits_inside_wall']['0.001'] and round(r['orbits_inside_wall']['0.001'])}")

    r = run_circular(0.25, 100.0, eps_bars=(), spurious_e=True)
    res["P9_spurious_e"] = r["max_e"]
    print(f"  P9 spurious e (two-flux drift, a0=100, nu=0.25): {r['max_e']:.2e}")

    print("== PN: merger-time deficit decomposition (nu=0.25, circular) ==")
    res["PN"] = pn_block()
    for r in res["PN"]:
        print(f"  a0={r['a0']:.0f}M: odevsN={100*(r['t_newton_ode']/r['t_newton_closed']-1):+.2f}% "
              f"flux1pn {r['flux_deficit_pct']:+.1f}%  geometry {r['geometry_pct']:+.1f}%  "
              f"both {r['both_pct']:+.1f}%")

    with open("inspiral-out.json", "w") as f:
        json.dump(res, f, indent=1, default=float)
    print("wrote inspiral-out.json")
