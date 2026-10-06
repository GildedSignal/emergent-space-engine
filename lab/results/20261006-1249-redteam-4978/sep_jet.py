#!/usr/bin/env python3
"""Red-team 20261006-1249: the jet (kick -> cycle via stored derivatives) near the
Schwarzschild separatrix. Exact equatorial Schwarzschild geodesics, M = 1, float64.

Truth: first integral u'^2 = F(u) = [E^2 - (1-2u)(1+L^2 u^2)] / L^2, factored by its
roots; per-radial-cycle dphi, dtau, dt by smooth quadrature in Darwin angle.
Jet: first-order Taylor of (dphi, dt) in L at fixed E, given the EXACT derivative
(best case for the design). Floor: 1e-6 (df81's re-anchor floor).
"""
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq, fsolve

FLOOR = 1e-6

def roots_poly(E, L):
    """real roots of p(u) = E^2 - (1-2u)(1+L^2 u^2), ascending"""
    r = np.roots([2 * L * L, -L * L, 2.0, E * E - 1.0])
    return np.sort(r.real[np.abs(r.imag) < 1e-9 * (1 + np.abs(r.real))])

def cycle(E, L):
    """per-radial-cycle (dphi, dtau, dt) for a bound orbit; None if not bound."""
    r = roots_poly(E, L)
    if len(r) != 3 or r[0] <= 0 or r[1] >= 0.5:
        return None
    ua, up, u3 = r
    K = np.sqrt(2.0)  # F = 2 (u-ua)(up-u)(u3-u); no L in sqrt(F)
    D = up - ua
    def ints(th):
        u = ua + D * np.sin(th) ** 2
        w = 2.0 / (K * np.sqrt(u3 - u))
        return w, w / (L * u * u), w * E / (L * u * u * (1 - 2 * u))
    tot = np.zeros(3)
    for j in range(3):
        tot[j] = 2.0 * quad(lambda t: ints(t)[j], 0, np.pi / 2,
                            epsabs=1e-13, epsrel=1e-13, limit=400)[0]
    return dict(dphi=tot[0], dtau=tot[1], dt=tot[2], ua=ua, up=up, u3=u3)

def jet_err(E, L0, eps, h=1e-8):
    """exact cycle at L0(1+eps) vs first-order Taylor at L0 (exact derivative)."""
    c0 = cycle(E, L0)
    if c0 is None:
        return None
    L1 = L0 * (1 + eps)
    c1 = cycle(E, L1)
    if c1 is None:
        return None
    cs = [cycle(E, L0 + k * h * L0) for k in (-2, -1, 1, 2)]
    if any(c is None for c in cs):
        return None
    out = {}
    for key in ("dphi", "dt"):
        fp1, fp2, fm1, fm2 = cs[2][key], cs[3][key], cs[1][key], cs[0][key]
        der = (-fp2 + 8 * fp1 - 8 * fm1 + fm2) / (12 * h * L0)  # 5-point stencil
        jet = c0[key] + der * (L1 - L0)
        out[key] = (c1[key] - jet, der)
    return dict(c0=c0, c1=c1, err_phi=out["dphi"][0], err_t=out["dt"][0],
                dphi1=out["dphi"][1])

def e_crit(L):
    """separatrix (unstable-circular) energy at this L"""
    u_star = brentq(lambda u: 1.0 / (u - 3 * u * u) - L * L, 1 / 6 + 1e-12, 1 / 3 - 1e-12)
    return np.sqrt((1 - 2 * u_star) ** 2 / (1 - 3 * u_star)), u_star

def l_crit(E):
    """separatrix (critical) L at this energy"""
    u_star = brentq(lambda u: (1 - 2 * u) ** 2 / (1 - 3 * u) - E * E, 1 / 6 + 1e-12, 0.25)
    return 1.0 / np.sqrt(u_star - 3 * u_star ** 2), u_star
def plunge_phi(E, L):
    """azimuth swept from the last turning point to the horizon u=1/2, plunging (E,L)."""
    r = roots_poly(E, L)
    ua = float(r[0])
    coef = np.poly1d([2 * L * L, -L * L, 2.0, E * E - 1.0])
    q = np.poly1d(np.polydiv(coef.c, [1.0, -ua])[0])  # p(u) = 2 (u - ua) q(u)
    def g(th):
        u = ua + (0.5 - ua) * np.sin(th) ** 2
        return np.sqrt(2 * (0.5 - ua)) * np.cos(th) * L / np.sqrt(max(q(u), 1e-300))
    return quad(g, 0, np.pi / 2, epsabs=1e-13, epsrel=1e-13, limit=400)[0], ua

def orbit_from_turning(rp, ra):
    """(E, L) for a Newtonian-style orbit with given pericenter/apocenter radii"""
    up_w, ua_w = 1 / rp, 1 / ra
    s = fsolve(lambda x: [(1 - 2 * up_w) * (1 + x[1] ** 2 * up_w ** 2) - x[0] ** 2,
                          (1 - 2 * ua_w) * (1 + x[1] ** 2 * ua_w ** 2) - x[0] ** 2],
               [1.0, 0.5 * (up_w + ua_w) / (up_w * ua_w)])
    return abs(s[0]), abs(s[1])

# ---------- instrument controls ----------
print("== instrument controls ==")
E0, L0 = 0.96, 3.7
c = cycle(E0, L0)
up = c["up"]
sol = solve_ivp(lambda phi, y: [y[1], 1.0 / L0 ** 2 + 3 * y[0] * y[0] - y[0]],
                [0, 4 * c["dphi"]], [up, 0.0], rtol=1e-12, atol=1e-14, max_step=1e-3)
ph, uu, vv = sol.t, sol.y[0], sol.y[1]
per = [ph[i] for i in range(50, len(ph) - 1)
       if uu[i] > uu[i - 1] and uu[i] >= uu[i + 1] and vv[i] > 0 > vv[i + 1]]
print(f"C1 RK pericenter spacings: {[f'{p:.9f}' for p in np.diff(per[:3])]}")
print(f"C1 quadrature dphi       : {c['dphi']:.9f}")
Ew, Lw = orbit_from_turning(100 * (1 - 0.5), 100 * (1 + 0.5))
cw = cycle(Ew, Lw)
print(f"C2 weak-field dphi-2pi = {cw['dphi'] - 2 * np.pi:.6f} vs 1PN 6*pi/p = "
      f"{6 * np.pi / 75:.6f}")

# ---------- family A: fixed L = 3.7, E -> E_sep^- (pure homoclinic) ----------
print("\n== family A: L = 3.7, E = E_sep*(1-delta), torque kick eps=1e-3 ==")
Ec, u_star = e_crit(3.7)
print(f"E_sep(3.7) = {Ec:.6f}, whirl radius {1 / u_star:.3f} M "
      f"(bound band: E in (E_stable_circ, E_sep))")
print(f"{'delta':>8} {'r_peri/M':>9} {'r_apo/M':>9} {'dphi':>10} {'orbits/cyc':>10} "
      f"{'err_phi':>10} {'x floor':>9} {'err_dt':>11} {'x floor':>9}")
for delta in (0.01, 0.005, 0.003, 0.001, 0.0003, 0.0001):
    E0 = Ec * (1 - delta)
    res = jet_err(E0, 3.7, 1e-3)
    if res is None:
        print(f"{delta:8.4f}  no bound orbit"); continue
    c0 = res["c0"]
    print(f"{delta:8.4f} {1 / c0['up']:9.3f} {1 / c0['ua']:9.3f} {c0['dphi']:10.3f} "
          f"{c0['dphi'] / 2 / np.pi:10.2f} {res['err_phi']:10.3e} "
          f"{abs(res['err_phi']) / FLOOR:9.1e} {res['err_t']:11.3e} "
          f"{abs(res['err_t']) / FLOOR:9.1e}")

# ---------- family B: fixed u_p = 1/4 (r_peri = 4 M), L -> 4^- ----------
print("\n== family B: r_peri = 4 M fixed, L = 4*(1-delta), torque kick eps=1e-3 ==")
print(f"{'delta':>8} {'E':>9} {'dphi':>10} {'orbits/cyc':>10} {'err_phi':>10} {'x floor':>9}")
for delta in (0.12, 0.05, 0.01, 0.003, 0.001):
    L0 = 4.0 * (1 - delta)
    E0 = np.sqrt((1 - 0.5) * (1 + L0 ** 2 * 0.0625))
    res = jet_err(E0, L0, 1e-3)
    if res is None:
        print(f"{delta:8.3f}  no bound orbit"); continue
    c0 = res["c0"]
    print(f"{delta:8.3f} {E0:9.6f} {c0['dphi']:10.3f} {c0['dphi'] / 2 / np.pi:10.2f} "
          f"{res['err_phi']:10.3e} {abs(res['err_phi']) / FLOOR:9.1e}")

# ---------- P3/P5 controls that must pass ----------
print("\n== controls (must pass) ==")
Ew, Lw = orbit_from_turning(45, 55)  # a=50M, e=0.1
res = jet_err(Ew, Lw, 1e-3)
print(f"P3a r_peri=45M e=0.1: dphi={res['c0']['dphi']:.6f} err_phi={res['err_phi']:.3e} "
      f"({abs(res['err_phi']) / FLOOR:.1e} x floor) err_dt={res['err_t']:.3e}")
Ew, Lw = orbit_from_turning(50, 4950)  # r_p=50M, e=0.98 near-parabolic
res = jet_err(Ew, Lw, 1e-3)
print(f"P5  r_peri=50M e=0.98: E={Ew:.8f} dphi-2pi={res['c0']['dphi'] - 2 * np.pi:.3e} "
      f"err_phi={res['err_phi']:.3e} ({abs(res['err_phi']) / FLOOR:.1e} x floor)")

# ---------- P4: regime flip ----------
print("\n== P4: bound -> plunge across the separatrix ==")
E0 = Ec * (1 - 0.005)
L0 = 3.7
res = jet_err(E0, L0, 1e-3)
Lsep, u_star = l_crit(E0)
L1 = Lsep * 0.998  # just across the separatrix (plunge side: L < L_sep at this E)
kick = (L1 - L0) / L0
print(f"orbit: E={E0:.6f} L0={L0}, L_sep(E)={Lsep:.6f}; applied kick dL/L = {kick:.4f}")
phi_jet = res["c0"]["dphi"] + res["dphi1"] * (L1 - L0)
print(f"jet predicts next pericenter after dphi_jet = {phi_jet:.1f} rad "
      f"({phi_jet / 2 / np.pi:.1f} orbits of phase)")
phi_h, ua = plunge_phi(E0, L1)
print(f"truth: plunge (roots {roots_poly(E0, L1)}); horizon reached after {phi_h:.2f} rad")
