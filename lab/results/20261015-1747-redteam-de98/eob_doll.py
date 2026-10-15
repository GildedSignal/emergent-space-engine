#!/usr/bin/env python3
"""Two-body doll ν-blindness at strong field — premise red-team 20261015-1747. v3.

representation.md §1 / r3 v3: "the relative motion is a test body in Schwarzschild
with M = m1+m2; ν enters only through the energy map", E_real/μ = (1/ν)√(1+2ν(E_eff−1)).
Inverting exactly at fixed ν (with ĥ ≡ Ĥ = (H−Mc²)/μ, E_real/μ = 1/ν + ĥ):

    E_eff = 1 + ĥ + (ν/2)·ĥ²        (map inversion; ν→0 gives the geodesic E)

Reference: the reduced ADM 2PN Hamiltonian (Damour–Jaranowski–Schäfer; Schäfer &
Jaranowski 2018 review Eq. 6.7–6.9), centre of mass, r = R/(GM), p = p₁/μ, c = 1:

  Ĥ = p²/2 − 1/r
    + (3ν−1)p⁴/8 − [(3+ν)p² + ν p_r²]/(2r) + 1/(2r²)
    + (1−5ν+5ν²)p⁶/16 + [(5−20ν−3ν²)p⁴ − 2ν²p_r²p² − 3ν²p_r⁴]/(8r)
      + [(5+8ν)p² + 3ν p_r²]/(2r²) − (1+3ν)/(4r³)

Doll: exact Schwarzschild geodesic (M=1) at the SAME real invariants (1/ν+ĥ, j),
i.e. geodesic (E_eff, L=j). Advance k and radial period T by radial quadratures
with the sine substitution r = mid + half·sinθ (removes turning-point singularities).

Controls: C1 doll quadrature vs closed form (1−6/p̄)^(−1/2)−1;
C2 ν→1e-6 row = the reference's own truncation floor (reported beside every error);
C3 doll ISCO r=6, Ω=6^(−3/2).
"""
import json
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, fsolve

EPS = 1e-30


def H_adm(r, pr, j, nu, order=2):
    p2 = pr * pr + j * j / (r * r)
    H = 0.5 * p2 - 1.0 / r
    H = H + (3 * nu - 1) * p2**2 / 8.0 - ((3 + nu) * p2 + nu * pr * pr) / (2.0 * r) + 1.0 / (2 * r * r)
    if order >= 2:
        H2 = (1 - 5 * nu + 5 * nu * nu) * p2**3 / 16.0
        H2 += ((5 - 20 * nu - 3 * nu * nu) * p2**2 - 2 * nu * nu * pr * pr * p2
               - 3 * nu * nu * pr**4) / (8.0 * r)
        H2 += ((5 + 8 * nu) * p2 + 3 * nu * pr * pr) / (2.0 * r * r)
        H2 -= (1 + 3 * nu) / (4.0 * r**3)
        H = H + H2
    return H


def dH(which, r, pr, j, nu, order):
    if which == "j":
        return H_adm(r, pr, j + EPS * 1j, nu, order).imag / EPS
    if which == "r":
        return H_adm(r + EPS * 1j, pr, j, nu, order).imag / EPS
    return H_adm(r, pr + EPS * 1j, j, nu, order).imag / EPS


def newton_turning_guesses(hhat, j):
    """Newtonian r_p, r_a from ĥ r² + r − j²/2 = 0 (ĥ<0 for bound)."""
    disc = np.sqrt(1.0 + 2.0 * hhat * j * j)
    ra = (-1.0 - disc) / (2.0 * hhat)
    rp = (-1.0 + disc) / (2.0 * hhat)
    return rp, ra


def solve_turning(g, rp0, ra0):
    """Two roots of g(r)=0 near Newtonian guesses; None if not bracketed/bound."""
    try:
        rp = brentq(g, 0.6 * rp0, min(1.4 * rp0, rp0 + 0.35 * (ra0 - rp0)), xtol=1e-14, rtol=1e-15)
        ra = brentq(g, max(0.6 * ra0, ra0 - 0.35 * (ra0 - rp0)), 1.4 * ra0, xtol=1e-14, rtol=1e-15)
    except ValueError:
        return None
    if ra <= rp * 1.0000001:
        return None
    mid = 0.5 * (rp + ra)
    if g(mid) > 0:  # not an allowed region
        return None
    return rp, ra


def pr_of_r(r, hhat, j, nu, order):
    f = lambda pr: H_adm(r, pr, j, nu, order) - hhat
    lo, hi = 0.0, 30.0
    if f(lo) > 0 or f(hi) < 0:
        return None
    for _ in range(64):
        mid = 0.5 * (lo + hi)
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def adm_k_T(hhat, j, nu, order=2):
    g = lambda r: H_adm(r, 0.0, j, nu, order) - hhat
    rp0, ra0 = newton_turning_guesses(hhat, j)
    if hhat >= 0 or not np.isfinite(rp0):
        return None
    tp = solve_turning(g, rp0, ra0)
    if tp is None:
        return None
    rp, ra = tp
    mid, half = 0.5 * (ra + rp), 0.5 * (ra - rp)

    def ph(theta):
        r = mid + half * np.sin(theta)
        pr = pr_of_r(r, hhat, j, nu, order)
        if pr is None or pr < 1e-290:
            return 0.0
        return (dH("j", r, pr, j, nu, order) / dH("pr", r, pr, j, nu, order)) * half * np.cos(theta)

    def tm(theta):
        r = mid + half * np.sin(theta)
        pr = pr_of_r(r, hhat, j, nu, order)
        if pr is None or pr < 1e-290:
            return 0.0
        return half * np.cos(theta) / dH("pr", r, pr, j, nu, order)

    dphi, _ = quad(ph, -np.pi / 2, np.pi / 2, limit=300, epsabs=1e-13, epsrel=1e-11)
    T, _ = quad(tm, -np.pi / 2, np.pi / 2, limit=300, epsabs=1e-13, epsrel=1e-11)
    return dphi / np.pi - 1.0, 2 * T, rp, ra


def doll_turning(E, L):
    f = lambda r: (1 - 2.0 / r) * (1 + L * L / (r * r)) - E * E
    grid = np.linspace(2.000001, 2000.0, 400000)
    vals = f(grid)
    roots = []
    idx = np.where(vals[:-1] * vals[1:] < 0)[0]
    for i in idx:
        roots.append(brentq(f, grid[i], grid[i + 1], xtol=1e-14, rtol=1e-15))
    if len(roots) < 2:
        return None
    rp, ra = roots[-2], roots[-1]
    if f(0.5 * (rp + ra)) > 0:
        return None
    return rp, ra


def doll_k_T(E, L):
    tp = doll_turning(E, L)
    if tp is None:
        return None
    rp, ra = tp
    mid, half = 0.5 * (ra + rp), 0.5 * (ra - rp)

    def ph(theta):
        r = mid + half * np.sin(theta)
        s = E * E - (1 - 2.0 / r) * (1 + L * L / (r * r))
        if s <= 0:
            return 0.0
        return L / (r * r) / np.sqrt(s) * half * np.cos(theta)

    def tm(theta):
        r = mid + half * np.sin(theta)
        s = E * E - (1 - 2.0 / r) * (1 + L * L / (r * r))
        if s <= 0:
            return 0.0
        return E / (1 - 2.0 / r) / np.sqrt(s) * half * np.cos(theta)

    dphi, _ = quad(ph, -np.pi / 2, np.pi / 2, limit=300, epsabs=1e-13, epsrel=1e-11)
    T, _ = quad(tm, -np.pi / 2, np.pi / 2, limit=300, epsabs=1e-13, epsrel=1e-11)
    return dphi / np.pi - 1.0, 2 * T, rp, ra


def adm_orbit_label(pbar, e, nu, order=2):
    rp_t, ra_t = pbar / (1 + e), pbar / (1 - e)
    h0 = -(1 - e * e) / (2 * pbar)
    j0 = float(np.sqrt(pbar))

    def F(x):
        hhat, j = x
        if j <= 0:
            return [1e3, 1e3]
        g = lambda r: H_adm(r, 0.0, j, nu, order) - hhat
        tp = solve_turning(g, *newton_turning_guesses(hhat, j))
        if tp is None:
            return [1e3, 1e3]
        return [tp[0] - rp_t, tp[1] - ra_t]

    sol = fsolve(F, [h0, j0], xtol=1e-13, maxfev=400)
    if not np.all(np.isfinite(sol)) or sol[1] <= 0:
        return None
    return float(sol[0]), float(sol[1])


def compare(pbar, e, nu):
    out = {"pbar": pbar, "e": e, "nu": nu}
    lab = adm_orbit_label(pbar, e, nu)
    if lab is None:
        return None
    hhat, j = lab
    out["hhat"], out["j"] = hhat, j
    E_eff = 1.0 + hhat + 0.5 * nu * hhat * hhat  # the design's energy map, inverted
    out["E_eff"] = E_eff
    ref = adm_k_T(hhat, j, nu)
    if ref is None:
        return None
    out["k_ref"], out["T_ref"] = ref[0], ref[1]
    dol = doll_k_T(E_eff, j) if E_eff < 1.0 else None
    if dol is None:
        out["doll_plunge_fabricated"] = True
        return out
    out["doll_plunge_fabricated"] = False
    out["k_doll"], out["T_doll"] = dol[0], dol[1]
    out["ek"] = (dol[0] - ref[0]) / ref[0]
    out["eT"] = (dol[1] - ref[1]) / ref[1]
    lab0 = adm_orbit_label(pbar, e, 1e-6)
    if lab0 is not None:
        h0, j0 = lab0
        E0 = 1.0 + h0 + 0.5e-6 * h0 * h0
        r0 = adm_k_T(h0, j0, 1e-6)
        d0 = doll_k_T(E0, j0) if E0 < 1.0 else None
        if r0 is not None and d0 is not None:
            out["ek_base"] = (d0[0] - r0[0]) / r0[0]
            out["eT_base"] = (d0[1] - r0[1]) / r0[1]
    return out


def rk_advance_doll(E, L, phi_max=60.0):
    """Independent check: integrate u'' = -u + 1/L^2 + 3u^2, return k."""
    from scipy.integrate import solve_ivp
    from scipy.optimize import brentq
    f = lambda r: (1 - 2.0 / r) * (1 + L * L / (r * r)) - E * E
    grid = np.linspace(2.000001, 2000.0, 400000)
    vals = f(grid)
    roots = []
    for i in np.where(vals[:-1] * vals[1:] < 0)[0]:
        roots.append(brentq(f, grid[i], grid[i + 1], xtol=1e-14, rtol=1e-15))
    up = 1.0 / roots[-2]
    rhs = lambda phi, y: [y[1], -y[0] + 1.0 / (L * L) + 3.0 * y[0] * y[0]]
    s0 = solve_ivp(rhs, [0, 0.02], [up, 0.0], rtol=1e-13, atol=1e-15)
    ev = lambda phi, y: y[1]  # du crosses 0 downward at perihelion
    ev.direction = -1; ev.terminal = True
    sol = solve_ivp(rhs, [0.02, phi_max], s0.y[:, -1], events=ev,
                    rtol=1e-13, atol=1e-15, max_step=0.02)
    if len(sol.t_events[0]) == 0:
        return None
    return sol.t_events[0][0] / (2 * np.pi) - 1


def rk_advance_adm(hhat, j, nu, order=2):
    """Independent check: integrate ADM Hamilton equations for (r, phi)."""
    from scipy.integrate import solve_ivp
    tp = adm_k_T.__wrapped__ if False else None
    g = lambda r: H_adm(r, 0.0, j, nu, order) - hhat
    tp = solve_turning(g, *newton_turning_guesses(hhat, j))
    if tp is None:
        return None
    rp = tp[0]
    pr = 1e-9
    def rhs(t, y):
        r, phi, pr_ = y
        return [dH('pr', r, pr_, j, nu, order), dH('j', r, pr_, j, nu, order), -dH('r', r, pr_, j, nu, order)]
    def peri(t, y):
        return y[2]
    peri.direction = 1; peri.terminal = True
    s0 = solve_ivp(rhs, [0, 0.05], [rp, 0.0, 1e-9], rtol=1e-13, atol=1e-15)
    sol = solve_ivp(rhs, [0.05, 200.0], s0.y[:, -1], events=peri, rtol=1e-13, atol=1e-15, max_step=0.05)
    if len(sol.t_events[0]) < 2:
        return None
    return sol.t_events[0][1] / (2 * np.pi) - 1

def main():
    R = {}
    # C1: doll quadrature vs independent RK orbit integration
    c1 = []
    for pbar, e in [(20, 0.6), (12, 0.3), (8.5, 0.1), (50, 0.9)]:
        rp0, ra0 = pbar / (1 + e), pbar / (1 - e)
        F = lambda x: [(1 - 2 / rp0) * (1 + x[1] ** 2 / rp0 ** 2) - x[0] ** 2,
                       (1 - 2 / ra0) * (1 + x[1] ** 2 / ra0 ** 2) - x[0] ** 2]
        E, L = fsolve(F, [np.sqrt(1 - 2 / ra0), np.sqrt(pbar)])
        dq = doll_k_T(E, L)
        k_rk = rk_advance_doll(E, L, phi_max=400.0)
        if dq is None or k_rk is None:
            c1.append(dict(pbar=pbar, e=e, relerr=None))
            continue
        k_quad = dq[0]
        c1.append(dict(pbar=pbar, e=e, k_quad=k_quad, k_rk=k_rk,
                       relerr=abs(k_quad - k_rk) / abs(k_rk)))
    R["C1"] = c1
    print("C1 doll quad vs RK relerr:", [f"{c['relerr']:.2e}" if c["relerr"] is not None else "?" for c in c1])

    # C1b: ADM quadrature vs independent ADM RK integration (nu=0.25)
    c1b = []
    for pbar, e in [(20, 0.6), (12, 0.3)]:
        lab = adm_orbit_label(pbar, e, 0.25)
        if lab is None:
            continue
        hhat, j = lab
        q = adm_k_T(hhat, j, 0.25)
        if q is None:
            c1b.append(dict(pbar=pbar, e=e, relerr=None))
            continue
        kq, Tq, _, _ = q
        kr = rk_advance_adm(hhat, j, 0.25)
        c1b.append(dict(pbar=pbar, e=e, k_quad=kq, k_rk=kr,
                        relerr=abs(kq - kr) / abs(kr) if kr else None))
    R["C1b"] = c1b
    print("C1b ADM quad vs RK relerr:", [f"{c['relerr']:.2e}" if c['relerr'] else "?" for c in c1b])

    p1 = [compare(20, 0.6, 0.25), compare(20, 0.3, 0.25), compare(30, 0.6, 0.25)]
    R["P1"] = p1
    print("P1 ecfd cross-check (ν=0.25):")
    for r in p1:
        if r is None:
            print("   label failed")
            continue
        if "ek" in r:
            print(f"   p̄={r['pbar']:>4} e={r['e']}  ek={r['ek']:+.4%} (base {r.get('ek_base', float('nan')):+.4%})"
                  f"  eT={r['eT']:+.4%} (base {r.get('eT_base', float('nan')):+.4%})")
        else:
            print(f"   p̄={r['pbar']:>4} e={r['e']}  DOLL PLUNGE FABRICATED (E_eff={r['E_eff']:.4f})")

    sweep = []
    for nu in (0.25, 0.1, 0.01):
        for e in (0.1, 0.3, 0.6, 0.9):
            for pbar in (8, 10, 12, 15, 20, 30, 50, 80, 120):
                if e == 0.9 and pbar < 12:
                    continue
                r = compare(pbar, e, nu)
                if r:
                    sweep.append(r)
    R["sweep"] = sweep
    print("\nSweep ek raw[minus ν=1e-6 base], eT raw:")
    for nu in (0.25, 0.1, 0.01):
        print(f" ν={nu}")
        for e in (0.1, 0.3, 0.6, 0.9):
            line = f"  e={e}: "
            for s in [r for r in sweep if r["nu"] == nu and r["e"] == e]:
                if "ek" not in s:
                    line += f"p̄{s['pbar']}:PLUNGE* "
                else:
                    b = s.get("ek_base")
                    cor = s["ek"] - b if b is not None else float("nan")
                    line += f"p̄{s['pbar']:<4g}:{s['ek']*100:+6.2f}%[{cor*100:+5.2f}] "
            print(line)
        for e in (0.1, 0.3, 0.6, 0.9):
            line = f"  eT e={e}: "
            for s in [r for r in sweep if r["nu"] == nu and r["e"] == e]:
                if "eT" in s:
                    b = s.get("eT_base")
                    cor = s["eT"] - b if b is not None else float("nan")
                    line += f"p̄{s['pbar']:<4g}:{s['eT']*100:+6.2f}%[{cor*100:+5.2f}] "
            print(line)

    print("\nP5 circular separatrix (M=1 units): doll r_ISCO=6, Ω=6^-1.5=%.6f" % 6.0**-1.5)
    p5 = []
    for nu in (0.25, 0.1, 0.01):
        rows, rows3 = [], []
        for r in np.linspace(2.5, 60.0, 4000):
            for order, acc in ((2, rows), (3, rows3)):
                f = lambda j: H_adm(r + 1e-6, 0.0, j, nu, order) - H_adm(r - 1e-6, 0.0, j, nu, order)
                try:
                    j = brentq(f, 1e-3, 60.0, xtol=1e-13)
                except ValueError:
                    continue
                Om = dH("j", r, 0.0, j, nu, order)
                if Om > 0:
                    acc.append((r, Om))
        if not rows:
            continue
        arr = np.array(rows)
        i = int(np.argmax(arr[:, 1]))
        arr3 = np.array(rows3) if rows3 else None
        i3 = int(np.argmax(arr3[:, 1])) if rows3 else None
        row = {"nu": nu,
               "adm_r_isco": float(arr[i, 0]), "adm_Om": float(arr[i, 1]),
               "adm3_r_isco": float(arr3[i3, 0]) if rows3 else None,
               "adm3_Om": float(arr3[i3, 1]) if rows3 else None,
               "dOm_doll_vs_adm": (6.0**-1.5 - arr[i, 1]) / arr[i, 1],
               "dr_doll_vs_adm": 6.0 - arr[i, 0]}
        if rows3:
            row["dOm_adm3_vs_adm2"] = (arr3[i3, 1] - arr[i, 1]) / arr[i, 1]
        p5.append(row)
        print(f"  ν={nu}: ADM2PN r_ISCO={row['adm_r_isco']:.4f} Ω={row['adm_Om']:.6f}"
              + (f" | ADM3PN r={row['adm3_r_isco']:.4f} Ω={row['adm3_Om']:.6f}" if rows3 else ""))
        print(f"        dΩ(doll−ADM2)/ADM2={row['dOm_doll_vs_adm']:+.2%}"
              + (f"  bracket dΩ(3PN−2PN)/2PN={row['dOm_adm3_vs_adm2']:+.2%}" if rows3 else "")
              + f"  Δr(doll−ADM2)={row['dr_doll_vs_adm']:+.4f}M")
    R["P5"] = p5

    census = {}
    for nu in (0.25, 0.1, 0.01):
        fab = tot = 0
        for pbar in np.linspace(6.7, 8.0, 27):
            r = compare(float(pbar), 0.3, nu)
            if r and "k_ref" in r:
                tot += 1
                fab += 1 if r.get("doll_plunge_fabricated") else 0
        census[str(nu)] = [fab, tot]
        print(f"fabricated-plunge census (e=0.3, p̄ 6.7–8.0, ν={nu}): {fab}/{tot}")
    R["census"] = census

    with open("eob_data.json", "w") as f:
        json.dump(R, f, indent=1, default=float)


if __name__ == "__main__":
    main()
