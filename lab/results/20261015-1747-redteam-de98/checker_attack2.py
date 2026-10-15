#!/usr/bin/env python3
"""Round 2: correct exact-isotropic control; phi-parametrized ADM RK (proper C1b)."""
import sys
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, ".")
import eob_doll as I

print("== A. exact isotropic test-mass H (correct form E^2 = a^2(1 + p^2/psi^4)) vs H_adm(nu=0) ==")
def H_exact_iso(r, pr, j):
    w = 0.5 / r
    a = (1 - w) / (1 + w)
    psi4 = (1 + w) ** 4
    p2 = pr * pr + j * j / (r * r)
    return a * np.sqrt(1.0 + p2 / psi4)
rows = []
for (r, pr, j) in [(12.0, 0.3, 4.4), (50.0, 0.05, 7.0), (30.0, 0.2, 5.0)]:
    h2 = I.H_adm(r, pr, j, 0.0, 2)
    he = H_exact_iso(r, pr, j)
    h1 = I.H_adm(r, pr, j, 0.0, 0)  # 1PN only
    rows.append((r, h1, h2, he))
    print(f"  r={r} pr={pr} j={j}: H_1PN={h1:.8f} H_2PN={h2:.8f} H_exact={he:.8f}"
          f" |1PN gap|={abs(h1-he):.2e} |2PN gap|={abs(h2-he):.2e} (2PN should shrink it)")

print("== B. ADM quadrature vs phi-parametrized RK (proper independent check) ==")
def rk_adm_phi(hhat, j, nu, phimax=200.0):
    def rhs(phi, y):
        r, pr_ = y
        dj = I.dH('j', r, pr_, j, nu, 2)
        return [I.dH('pr', r, pr_, j, nu, 2) / dj, -I.dH('r', r, pr_, j, nu, 2) / dj]
    g = lambda r: I.H_adm(r, 0.0, j, nu, 2) - hhat
    tp = I.solve_turning(g, *I.newton_turning_guesses(hhat, j))
    if tp is None:
        return None
    rp, ra = tp
    def peri(phi, y):
        return y[1]
    peri.direction = 1; peri.terminal = True
    s0 = solve_ivp(rhs, [0, 0.02], [rp, 0.0], rtol=1e-12, atol=1e-14)
    sol = solve_ivp(rhs, [0.02, phimax], s0.y[:, -1], events=peri, rtol=1e-12, atol=1e-14, max_step=0.01)
    if len(sol.t_events[0]) < 1:
        return None
    return sol.t_events[0][0] / (2 * np.pi) - 1.0
for pb, e, nu in [(20, 0.6, 0.25), (50, 0.6, 0.25), (20, 0.6, 1e-6), (30, 0.9, 0.1)]:
    hhat, j = I.adm_orbit_label(pb, e, nu)
    q = I.adm_k_T(hhat, j, nu)
    kr = rk_adm_phi(hhat, j, nu)
    if q and kr is not None:
        print(f"  pbar={pb} e={e} nu={nu}: quad k={q[0]:.8f} RK(phi) k={kr:.8f} rel={abs(q[0]-kr)/abs(kr):.2e}")
    else:
        print(f"  pbar={pb} e={e} nu={nu}: quad={q[0] if q else None} RK={kr} FAILED")

print("== C. e=0.99 grid artifact: raise doll grid to 20000, re-test ==")
orig = I.doll_turning
def doll_turning_wide(E, L):
    f = lambda r: (1 - 2.0 / r) * (1 + L * L / (r * r)) - E * E
    grid = np.linspace(2.000001, 20000.0, 400000)
    vals = f(grid)
    roots = []
    idx = np.where(vals[:-1] * vals[1:] < 0)[0]
    for i in idx:
        from scipy.optimize import brentq
        roots.append(brentq(f, grid[i], grid[i + 1], xtol=1e-14, rtol=1e-15))
    if len(roots) < 2:
        return None
    rp, ra = roots[-2], roots[-1]
    if f(0.5 * (rp + ra)) > 0:
        return None
    return rp, ra
I.doll_turning = doll_turning_wide
for pb in (30, 50):
    r = I.compare(pb, 0.99, 0.25)
    if r and "ek" in r:
        print(f"  pbar={pb} e=0.99 nu=0.25: fab={r['doll_plunge_fabricated']} corrected={(r['ek']-r['ek_base'])*100:+.2f}% baseline={r['ek_base']*100:+.2f}%")
    else:
        print(f"  pbar={pb} e=0.99: fab={r.get('doll_plunge_fabricated') if r else None}")
I.doll_turning = orig

print("== D. next-decade absolute-error scaling (is it nu/p^2 in absolute terms?) ==")
for nu in (0.25, 0.01):
    abs_errs = []
    for pb in (120, 200, 400):
        r = I.compare(pb, 0.6, nu)
        c = (r["ek"] - r["ek_base"]) * r["k_ref"]
        abs_errs.append((pb, c))
    (p1, c1), (p2, c2), (p3, c3) = abs_errs
    print(f"  nu={nu}: abs err @120/200/400 = {c1:.2e}/{c2:.2e}/{c3:.2e}"
          f" exponents {np.log(c1/c2)/np.log(200/120):.2f}, {np.log(c2/c3)/np.log(400/200):.2f} (2.0 = 1/p^2)")
