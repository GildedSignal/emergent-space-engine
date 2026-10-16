#!/usr/bin/env python3
"""Falsifier for representation.md SS3: 'Perturbations ... are kicks on E and L.
A cycle's derivatives are stored with it, so a kick updates the cycle by a
multiply-add.'

Instrument (float64): exact Schwarzschild equatorial cycle increments
C(E,L) = (dphi, dt, dtau) per radial cycle, by quadrature with a turning-point
substitution.  Arms:
  - recompile: C(E+dE, L+dL) exactly            (the shipped plane's path)
  - multiply-add: C + C_E dE + C_L dL           (the design's cheap path)
Error per channel, swept over orbit family (Darwin p,e), kick size (eps), and
direction; then a chained Peters-inspiral toy (stale vs refreshed derivatives
vs recompile).

Modes: validate | sweep | chain | all.  Deterministic.  <=60 s total.
"""
import sys
import json
import numpy as np
from scipy.integrate import quad

M = 1.0
TWOPI = 2.0 * np.pi


# ---------------------------------------------------------------- cycle C(E,L)
def turning_points(E, L):
    """Two largest physical roots of E^2 r^3 = (r-2)(r^2+L^2)."""
    c = [E * E - 1.0, 2.0, -L * L, 2.0 * L * L]  # r^3 E^2 - (r-2)(r^2+L^2)
    r = np.roots(c)
    re = sorted(x.real for x in r if abs(x.imag) < 1e-8 * max(1.0, abs(x)) and x.real > 2.0 + 1e-9)
    if len(re) < 2:
        return None
    return re[-2], re[-1]


def cycle(E, L, epsrel=1e-12):
    """(dphi, dt, dtau) for one radial cycle of the bound orbit (E,L)."""
    tp = turning_points(E, L)
    if tp is None:
        return None
    rp, ra = tp
    if ra - rp < 1e-6 * (ra + rp):  # circular limit, exact closed form
        r0 = 0.5 * (rp + ra)
        return np.array([TWOPI, TWOPI * r0 ** 1.5, TWOPI * r0 ** 1.5 * np.sqrt(1.0 - 3.0 / r0)])
    span = ra - rp

    def f(u, kind):
        s, c = np.sin(u), np.cos(u)
        r = rp + span * s * s
        V = (1.0 - 2.0 / r) * (1.0 + L * L / (r * r))
        d = E * E - V
        if d <= 0.0:
            return 0.0
        jac = 2.0 * span * s * c
        if kind == 0:  # phi
            return jac * (L / (r * r)) / np.sqrt(d)
        if kind == 1:  # t
            return jac * (E / (1.0 - 2.0 / r)) / np.sqrt(d)
        return jac / np.sqrt(d)  # tau

    out = np.empty(3)
    for k in range(3):
        out[k], _ = quad(f, 0.0, np.pi / 2, args=(k,), epsabs=0.0, epsrel=epsrel, limit=400)
    return 2.0 * out


def dcycle(E, L, hrel=1e-3):
    """5-point central derivatives dC/dE, dC/dL (3x2).

    Steps scale with the binding energy (1-E) for E and L for L: fractional
    probes on E unbind weak-field orbits, and (1-E) is the variation scale.
    Falls back to smaller steps if a probe leaves the bound domain.
    """
    for shrink in (1.0, 0.3, 0.1):
        hE, hL = hrel * shrink * (1.0 - E), hrel * shrink * L
        pts = [cycle(E + k * hE, L) for k in (-2, -1, 1, 2)] + \
              [cycle(E, L + k * hL) for k in (-2, -1, 1, 2)] + [cycle(E, L)]
        if any(p is None for p in pts):
            continue
        C0 = pts[8]
        d = np.empty((3, 2))
        d[:, 0] = (-pts[3] + 8 * pts[2] - 8 * pts[1] + pts[0]) / (12 * hE)
        d[:, 1] = (-pts[7] + 8 * pts[6] - 8 * pts[5] + pts[4]) / (12 * hL)
        return d
    return None


def EL_from_pe(p, e):
    """Darwin (p,e) -> exact (E,L) via the two turning points."""
    if e < 1e-9:  # circular: exact closed form
        r0 = p
        return np.sqrt((r0 - 2.0) ** 2 / (r0 * (r0 - 3.0))), r0 / np.sqrt(r0 - 3.0)
    rp, ra = p / (1.0 + e), p / (1.0 - e)
    A, B = 1.0 - 2.0 / rp, 1.0 - 2.0 / ra
    L2 = (A - B) / (B / (ra * ra) - A / (rp * rp))
    if L2 <= 0:
        return None
    E2 = A * (1.0 + L2 / (rp * rp))
    if not (0.0 < E2 < 1.0):
        return None
    return np.sqrt(E2), np.sqrt(L2)


def pe_from_EL(E, L):
    tp = turning_points(E, L)
    if tp is None:
        return None
    rp, ra = tp
    return (rp + ra) * 0.5, (ra - rp) / (ra + rp)


# ------------------------------------------------------------------- controls
def validate():
    rep = {}
    # 1. weak-field advance: dphi - 2pi -> 6*pi/p  (1PN), error = O(M^2/p^2)
    for p, e in ((1000.0, 0.5), (200.0, 0.6), (100.0, 0.0)):
        EL = EL_from_pe(p, e)
        C = cycle(*EL)
        if e == 0.0:
            r0 = p
            rep[f"circular_p{p:g}"] = dict(
                dphi=C[0] / TWOPI - 1.0,  # exactly 0
                dt_rel=C[1] / (TWOPI * r0 ** 1.5) - 1.0,
                dtau_rel=C[2] / (TWOPI * r0 ** 1.5 * np.sqrt(1 - 3.0 / r0)) - 1.0,
            )
        else:
            rep[f"advance_p{p:g}_e{e:g}"] = dict(
                gr_1pn=(C[0] - TWOPI) / (6.0 * np.pi / p),  # -> 1 + O(M/p)
                kepler_dt_rel=C[1] / (TWOPI * (p / (1 - e * e)) ** 1.5) - 1.0,
            )
    # 2. quadrature stability: epsrel 1e-13 vs 1e-11
    EL = EL_from_pe(8.0, 0.9)
    a, b = cycle(*EL, epsrel=1e-13), cycle(*EL, epsrel=1e-11)
    rep["quad_stability_p8_e0.9"] = np.abs(a / b - 1.0).max().item()
    # 3. derivative step robustness (Richardson)
    d1, d2 = dcycle(*EL, hrel=1e-5), dcycle(*EL, hrel=0.5e-5)
    rep["deriv_step_drift_p8_e0.9"] = np.abs(d1 / d2 - 1.0).max().item()
    # 4. second-order curvature coefficients (rel. error per kick ~ kappa*eps^2):
    #    Newtonian E-channel: kappa_E -> 15/8 exactly at large p (T ~ (1-E)^-3/2)
    #    1PN L-channel (advance): kappa_phi -> 18/(2 L^2 + 6)
    for p, e in ((1000.0, 0.6), (100.0, 0.6), (20.0, 0.3)):
        EL = EL_from_pe(p, e)
        E, L = EL
        C = cycle(E, L)
        hE, hL = 1e-3 * (1.0 - E), 1e-3 * L
        CEE = (cycle(E + hE, L) - 2 * C + cycle(E - hE, L)) / hE ** 2
        CLL = (cycle(E, L + hL) - 2 * C + cycle(E, L - hL)) / hL ** 2
        rep[f"kappa_p{p:g}_e{e:g}"] = dict(
            kappa_E=0.5 * abs(CEE) * (1 - E) ** 2 / C,
            kepler_kappa_E=15.0 / 8.0,
            kappa_L_phi=0.5 * abs(CLL[0]) * L ** 2 / C[0],
            analytic_1pn=18.0 / (2 * L * L + 6.0),
        )
    return rep
    return rep


# ----------------------------------------------------------------- the sweep
def one_kick(p, e, epsE, epsL):
    """Relative per-channel error of the multiply-add vs the exact recompile.

    Kick sizes: epsE is a fraction of the binding energy (1-E), epsL of L.
    """
    EL = EL_from_pe(p, e)
    if EL is None:
        return None
    E, L = EL
    C0 = cycle(E, L)
    D = dcycle(E, L)
    if C0 is None or D is None:
        return None
    dE, dL = epsE * (1.0 - E), epsL * L
    Ct = cycle(E + dE, L + dL)  # truth = recompile
    if Ct is None:
        return None  # kick left the bound domain
    Cma = C0 + D[:, 0] * dE + D[:, 1] * dL
    return np.abs(Cma / Ct - 1.0)


def sweep():
    ps = [6.5, 7.05, 8.0, 10.0, 20.0, 100.0, 1000.0]
    es = [0.0, 0.3, 0.6, 0.9, 0.99]
    epss = [1e-5, 1e-4, 1e-3, 1e-2, 1e-1]
    dirs = {"E": (1, 0), "L": (0, 1), "EL": (1, 1)}
    rows = []
    for p in ps:
        for e in es:
            if p < 6.0 + 2.0 * e + 0.02:
                continue  # separatrix guard
            for eps in epss:
                for name, (a, b) in dirs.items():
                    r = one_kick(p, e, a * eps, b * eps)
                    if r is None:
                        rows.append(dict(p=p, e=e, eps=eps, d=name, unbound_or_degenerate=True))
                        continue
                    rows.append(dict(p=p, e=e, eps=eps, d=name,
                                     err_phi=r[0], err_t=r[1], err_tau=r[2]))
    return rows


# ------------------------------------------------------- chained Peters toy
def peters_rates(a, e, nu):
    f = (1 + (73.0 / 24) * e * e + (37.0 / 96) * e ** 4) / (1 - e * e) ** 3.5
    g = (1 + (121.0 / 304) * e * e) / (1 - e * e) ** 2.5
    return (-(64.0 / 5) * nu / a ** 3 * f, -(304.0 / 15) * e * nu / a ** 4 * g)


def chain(p0, e0, nu=0.25, mode="recompile", refresh=1, max_cycles=5000, shared=False):
    """Inspiraling body: exact Schwarzschild cycle + Peters kicks per cycle.

    mode: 'recompile' (exact C each kick) or 'ma' (multiply-add, derivatives
    refreshed every `refresh` kicks; np.inf = stale).
    """
    EL = EL_from_pe(p0, e0)
    if EL is None:
        return None
    E, L = EL
    C = cycle(E, L)
    D = dcycle(E, L)
    phi = tau = t = 0.0
    n = 0
    trace = []
    while n < max_cycles:
        a, e = pe_from_EL(E, L)
        if a is None or e is None or (p := a * (1 - e * e)) <= 6.0 + 2.0 * e + 0.02:
            break
        adot, edot = peters_rates(a, e, nu)
        Ct = cycle(E, L) if shared else C  # shared: exact dt sizes kicks in every arm
        if Ct is None:
            break
        da, de = adot * Ct[1], edot * Ct[1]  # kick sized by the current cycle's dt
        a2, e2 = a + da, max(e + de, 0.0)
        EL2 = EL_from_pe(a2 * (1 - e2 * e2), e2)
        if EL2 is None:
            break
        E2, L2 = EL2
        dE, dL = E2 - E, L2 - L
        phi += C[0]; t += C[1]; tau += C[2]
        n += 1
        if mode == "recompile":
            C = cycle(E2, L2)
            if C is None:
                break
            D = dcycle(E2, L2)
        else:
            if refresh is not None and n % refresh == 0:
                C = cycle(E2, L2)
                D = dcycle(E2, L2)
            else:
                C = C + D[:, 0] * dE + D[:, 1] * dL
        if C is None or not np.all(np.isfinite(C)) or C[1] <= 0:
            break
        E, L = E2, L2
        if n <= 8 or n % 25 == 0:
            trace.append(dict(n=n, p=a * (1 - e * e), e=e, dphi=C[0], dt=C[1], dtau=C[2]))
    return dict(mode=mode, refresh=(None if mode == "recompile" else refresh),
                cycles=n, t_merge=t, phi_total=phi, tau_total=tau, p_end=a * (1 - e * e),
                e_end=e, trace=trace)


# ---------------------------------------------------------------------- main
def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    out = {}
    if mode in ("validate", "all"):
        out["validate"] = validate()
    if mode in ("sweep", "all"):
        rows = sweep()
        out["sweep_rows"] = len(rows)
        with open("sweep.json", "w") as fh:
            json.dump(rows, fh)
        # headline reductions
        ok = [r for r in rows if not r.get("unbound_or_degenerate")]
        def worst(sel, ch):
            v = [(r[ch], r) for r in ok if sel(r)]
            return max(v) if v else None
        bulk = lambda r: r["p"] >= 20 and r["e"] <= 0.9
        sep = lambda r: r["p"] - (6 + 2 * r["e"]) <= 0.5
        out["bulk_worst"] = {ch: worst(bulk, ch)[0] for ch in ("err_phi", "err_t", "err_tau")}
        out["sep_worst"] = {ch: worst(sep, ch) for ch in ("err_phi", "err_t", "err_tau")}
    if mode in ("chain", "all"):
        cs = {}
        for (p0, e0) in ((20.0, 0.3), (12.0, 0.6)):
            base = chain(p0, e0, mode="recompile")
            arms = {"recompile": base}
            for tag, ref in (("ma_stale", None), ("ma_r64", 64), ("ma_r8", 8)):
                arms[tag] = chain(p0, e0, mode="ma", refresh=ref)
            for tag, ref in (("ma_stale_sh", None), ("ma_r8_sh", 8)):
                arms[tag] = chain(p0, e0, mode="ma", refresh=ref, shared=True)
            cs[f"p{p0:g}_e{e0:g}"] = {k: {kk: vv for kk, vv in v.items() if kk != "trace"}
                                      for k, v in arms.items()}
        out["chains"] = cs
    print(json.dumps(out, indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o)))


if __name__ == "__main__":
    main()
