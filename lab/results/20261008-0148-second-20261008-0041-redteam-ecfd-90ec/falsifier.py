#!/usr/bin/env python3
"""Red-team 20261008-0041, decisive run.

Question: how far is the shipped two-body doll (exact Schwarzschild geodesic
+ 1PN EOB energy map, r3 v3 `eob-doll`) from GR at 2PN, at the gate's own
seeds (nu up to 0.25, p down to 20 M)?

All orbits are built from IDENTICAL geometric turning points (u_p, u_a),
so the comparison carries no coordinate or (p, e)-labeling ambiguity.

  shipped : exact Schwarzschild advance (geodesic ODE u''+u=1/L^2+3u^2),
            validated against the closed form 2*pi*(1/sqrt(1-6/p)-1)
            and against the e->0 limit.
  GR2PN   : 2PN EOB Hamiltonian, H_eff^2 = A(1+j^2 u^2) + F(u) u^4 pu^2,
            F = A^2*Dbar,  A = 1-2u+2*nu*u^3,  Dbar = 1+s*6*nu*u^2.
            Controls: nu->0 reproduces the exact advance (residual ~1e-6);
            Dbar sign flip moves the advance < 1e-3 relative (3PN term).
  oracle  : 6*pi/pbar, the 1PN family that r3 v3 / B11 judge against.

Controls on both sides: positive = nu->0 EOB == exact Schwarzschild;
negative = at pbar=1000 everything must agree with the published
weak-field expansion +4.5/pbar.
"""
import json
import numpy as np
from scipy.integrate import solve_ivp

RTOL, ATOL = 1e-13, 1e-16


def advance_exact(up, ua):
    invL2 = (up + ua) / 2 - (up * up + up * ua + ua * ua)
    def rhs(phi, y):
        u, up_ = y
        return [up_, invL2 + 3.0 * u * u - u]
    def peri(phi, y):
        return y[1]
    peri.direction = -1.0
    peri.terminal = True
    sol = solve_ivp(rhs, (0.0, 300.0), [up, -1e-9], method="DOP853",
                    rtol=RTOL, atol=ATOL, events=peri)
    return float(sol.t_events[0][0] - 2 * np.pi)


def advance_eob(nu, up, ua, order=2, s=+1):
    if order == 2:
        A  = lambda u: 1.0 - 2.0 * u + 2.0 * nu * u ** 3
        dA = lambda u: -2.0 + 6.0 * nu * u * u
        D  = lambda u: 1.0 + s * 6.0 * nu * u * u
        dD = lambda u: s * 12.0 * nu * u
    else:
        A  = lambda u: 1.0 - 2.0 * u
        dA = lambda u: -2.0
        D  = lambda u: 1.0
        dD = lambda u: 0.0
    F  = lambda u: A(u) ** 2 * D(u)
    dF = lambda u: 2 * A(u) * dA(u) * D(u) + A(u) ** 2 * dD(u)
    Ap, Aa = A(up), A(ua)
    j2 = (Aa - Ap) / (Ap * up ** 2 - Aa * ua ** 2)
    assert j2 > 0
    j = np.sqrt(j2)
    h = np.sqrt(A(up) * (1 + j2 * up ** 2))

    def rhs(phi, y):
        u, pu = y
        Au = A(u)
        dS_du = (dA(u) * (1.0 + j * j * u * u) + Au * 2.0 * j * j * u
                 + dF(u) * u ** 4 * pu * pu + F(u) * 4.0 * u ** 3 * pu * pu)
        return [F(u) * u ** 2 * pu / (j * Au), -dS_du / (2.0 * Au * j * u * u)]

    def peri(phi, y):
        return y[1]
    peri.direction = -1.0
    peri.terminal = True
    sol = solve_ivp(rhs, (0.0, 100.0), [up, -1e-9], method="DOP853",
                    rtol=RTOL, atol=ATOL, events=peri)
    # H_eff conservation check at the end
    u_e = sol.y[0, -1]; pu_e = sol.y[1, -1]
    H_end = np.sqrt(A(u_e) * (1 + j * j * u_e * u_e) + F(u_e) * u_e ** 4 * pu_e ** 2)
    return float(sol.t_events[0][0] - 2 * np.pi), float(abs(H_end - h) / h)


out = {"controls": {}}

# ---- controls ---------------------------------------------------------------
for pbar, e in [(50.0, 0.6), (20.0, 0.6), (100.0, 0.3)]:
    uc = 1 / pbar
    up, ua = uc * (1 + e), uc * (1 - e)
    a_ex = advance_exact(up, ua)
    a_cl = 2 * np.pi * (1 / np.sqrt(1 - 6 / pbar) - 1)
    a_eob0, dH = advance_eob(1e-9, up, ua, order=2, s=+1)
    out["controls"][f"pbar{pbar:g}_e{e:g}"] = {
        "exact_int": a_ex, "closed_e0": a_cl,
        "rel_int_vs_closed": abs(a_ex - a_cl) / a_cl,
        "eob_nu0": a_eob0, "rel_eob_nu0_vs_exact": abs(a_eob0 - a_ex) / a_ex,
        "eob_H_drift": dH}

# ---- decisive grid ----------------------------------------------------------
E = 0.6
grid = [20.0, 30.0, 50.0, 100.0, 200.0, 500.0, 1000.0]
nus = [0.01, 0.1, 0.25]
rows = []
for pbar in grid:
    uc = 1 / pbar
    up, ua = uc * (1 + E), uc * (1 - E)
    a_ship = advance_exact(up, ua)
    a_1pn = 6 * np.pi / pbar
    r = {"pbar": pbar, "e": E,
         "adv_shipped": a_ship,
         "adv_1pn_oracle": a_1pn,
         "rel_oracle_vs_shipped": (a_1pn - a_ship) / a_ship,
         "tol_B11_precession": 0.01 + 16.0 / pbar,
         "weak_field_pred": 4.5 / pbar}
    for nu in nus:
        # Dbar = 1 - 6*nu*u^2: the 2PN term of D = A*B (Damour, arXiv:1212.3169 eq. 19)
        a_gr, dH = advance_eob(nu, up, ua, order=2, s=-1)
        r[f"rel_shipped_vs_GR2PN_nu{nu:g}"] = (a_ship - a_gr) / a_gr
        if nu == 0.25:
            a_wrong, _ = advance_eob(nu, up, ua, order=2, s=+1)
            r["Dbar_sign_spread_nu0.25"] = abs(a_wrong - a_gr) / a_gr
            r["adv_GR2PN_nu0.25"] = a_gr
            r["drift_rad_per_orbit_nu0.25"] = a_ship - a_gr
    rows.append(r)
out["grid"] = rows

# ---- c2 fit -----------------------------------------------------------------
def fit_c2(f):
    ps = np.array([30.0, 40.0, 60.0, 80.0])
    g = np.array([f(p) / (6 * np.pi / p) - 1.0 for p in ps])
    X = np.vstack([1 / ps, 1 / ps ** 2]).T
    c, *_ = np.linalg.lstsq(X, g, rcond=None)
    return c[0]

out["c2"] = {
    "shipped_exact": fit_c2(lambda p: advance_exact((1 + E) / p, (1 - E) / p)),
    "GR2PN_nu0.25": fit_c2(lambda p: advance_eob(0.25, (1 + E) / p, (1 - E) / p, s=-1)[0]),
    "GR2PN_nu0.10": fit_c2(lambda p: advance_eob(0.10, (1 + E) / p, (1 - E) / p, s=-1)[0]),
    "GR2PN_nu0.01": fit_c2(lambda p: advance_eob(0.01, (1 + E) / p, (1 - E) / p, s=-1)[0]),
    "GR2PN_nu0.25_wrongsign": fit_c2(lambda p: advance_eob(0.25, (1 + E) / p, (1 - E) / p, s=+1)[0]),
}
out["c2"]["gap_shipped_vs_GR_nu0.25"] = (out["c2"]["shipped_exact"]
                                         - out["c2"]["GR2PN_nu0.25"])

print(json.dumps(out, indent=1))
with open("falsifier-out.json", "w") as f:
    json.dump(out, f, indent=1)
