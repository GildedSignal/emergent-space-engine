#!/usr/bin/env python3
"""Falsifier: the multiply-add cycle update (docs/representation.md L67) vs the
one-floor-unit error budget (L60), on the Schwarzschild separatrix family.

Truth = exact timelike geodesics (M=1, equatorial 2D), cycle map
(Dphi, Dt, Dtau) = periapsis-to-periapsis. Taylor update = C(E,L) + dC.d(E,L)
at one-quantum kicks. Budget = 2^-w * |Delta|. No repo code touched.
Runtime: < ~60 s single core, < 200 MB.
"""
import json
import math
import os
import sys

import numpy as np
from scipy.integrate import solve_ivp

M = 1.0
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")

# ---------------------------------------------------------------- geodesics
def invariants(p, e):
    """(E, L) for bound Schwarzschild geodesic r=p/(1+e cos chi)."""
    E = math.sqrt(((p - 2.0) ** 2 - 4.0 * e * e) / (p * (p - 3.0 - e * e)))
    L = p / math.sqrt(p - 3.0 - e * e)
    return E, L


def V(r, L):
    return (1.0 - 2.0 * M / r) * (1.0 + L * L / (r * r))


def dVdr(r, L):
    return (2.0 * M / (r * r)) * (1.0 + L * L / (r * r)) \
        + (1.0 - 2.0 * M / r) * (-2.0 * L * L / (r ** 3))


def turning_points(E, L):
    """Outer turning points (r_p, r_a) of R(r)=E^2-V; None if not bound.
    np.roots classifies; bisection polishes to full float precision."""
    # R(r) = (E^2-1) r^4 + 2 r^3 - L^2 r^2 + 2 L^2 r   (M=1)
    coeff = [E * E - 1.0, 2.0, -L * L, 2.0 * L * L, 0.0]
    roots = np.roots(coeff)
    rr = sorted(r.real for r in roots
                if abs(r.imag) < 1e-9 * max(1.0, abs(r.real)) and r.real > 2.0 * M)
    if len(rr) < 2:
        return None
    # the bound orbit's well is between the two LARGEST real roots
    rp0, ra0 = rr[-2], rr[-1]
    mid = math.sqrt(rp0 * ra0)

    def Rf(x):
        return E * E - V(x, L)

    if Rf(mid) <= 0.0:
        return None  # no allowed region between them: not a bound orbit

    def bisect(x_out):
        # R(x_out) < 0 < R(mid): root between
        lo, hi = x_out, mid
        if Rf(lo) > 0.0:
            return None
        for _ in range(100):
            m2 = 0.5 * (lo + hi)
            if Rf(m2) <= 0.0:
                lo = m2
            else:
                hi = m2
        return 0.5 * (lo + hi)

    rp = bisect(max(2.0 * M * 1.0000001, rp0 * (1.0 - 1e-3)))
    ra = bisect(ra0 * (1.0 + 1e-3))
    if rp is None or ra is None or not (rp < mid < ra):
        return None
    if Rf(0.5 * (rp + mid)) <= 0.0 or Rf(0.5 * (mid + ra)) <= 0.0:
        return None  # well not contiguous (should not happen for bound)
    return rp, ra


def rhs(tau, y, E, L):
    r, u = y[0], y[1]
    return [u, -0.5 * dVdr(r, L), L / (r * r), E / (1.0 - 2.0 * M / r)]



def hit_peri(tau, y, E=0.0, L=0.0):
    return y[1]  # u = dr/dtau


hit_peri.direction = 1.0  # crossing upward => periapsis
hit_peri.terminal = False


def hit_plunge(tau, y, E=0.0, L=0.0):
    return y[0] - 2.0 * M


hit_plunge.direction = -1.0
hit_plunge.terminal = True


def cycle(E, L, tag="", n=4096):
    """One radial cycle (periapsis to periapsis) via the exact first integrals.

    Substitution r = mid + half*cos(theta) cancels the algebraic endpoint
    weight exactly; midpoint rule over smooth h converges geometrically.
    """
    tp = turning_points(E, L)
    if tp is None:
        return {"bound": False, "tag": tag}
    rp, ra = tp
    mid = 0.5 * (rp + ra)
    half = 0.5 * (ra - rp)
    th = math.pi * (np.arange(n) + 0.5) / n
    r = mid + half * np.cos(th)
    R = E * E - (1.0 - 2.0 * M / r) * (1.0 + L * L / (r * r))
    # w = (r-rp)(ra-r) as (half*sin(theta))^2: cancellation-free
    w = (half * np.sin(th)) ** 2
    if np.any(R <= 0.0):
        return cycle_ode(E, L, tag)  # degenerate nodes: fall back to ODE
    s = np.sqrt(R / w)
    dphi = 2.0 * (math.pi / n) * np.sum(L / (r * r) / s)
    dt = 2.0 * (math.pi / n) * np.sum((E / (1.0 - 2.0 * M / r)) / s)
    dtau = 2.0 * (math.pi / n) * np.sum(1.0 / s)
    return {"bound": True, "dphi": float(dphi), "dt": float(dt),
            "dtau": float(dtau), "tag": tag}


def cycle_ode(E, L, tag=""):
    """Reference path: direct geodesic integration between two periapses."""
    tp = turning_points(E, L)
    if tp is None:
        return {"bound": False, "tag": tag}
    rp, ra = tp
    r0 = rp * (1.0 + 1e-9)
    u0sq = E * E - V(r0, L)
    eps = 1e-9
    while u0sq <= 0.0 and eps < 1e-3:
        eps *= 4.0
        r0 = rp * (1.0 + eps)
        u0sq = E * E - V(r0, L)
    u0 = math.sqrt(max(u0sq, 0.0))
    tau_max = 1000.0 * (ra ** 1.5) + 1e7
    sol = solve_ivp(rhs, (0.0, tau_max), [r0, u0, 0.0, 0.0], args=(E, L),
                    method="DOP853", rtol=1e-12, atol=1e-13,
                    events=[hit_peri, hit_plunge], dense_output=False,
                    max_step=math.inf)
    if sol.t_events[1].size > 0:
        return {"bound": False, "tag": tag}
    ev = sol.t_events[0]
    if ev.size < 2:  # need two clean periapsis crossings
        return {"bound": False, "tag": tag}
    y1 = sol.y_events[0][0]
    y2 = sol.y_events[0][1]
    return {"bound": True, "dphi": y2[2] - y1[2], "dt": y2[3] - y1[3],
            "dtau": ev[1] - ev[0], "tag": tag}


def richardson_d(f, x, h):
    """Central-difference derivative, Richardson-extrapolated (h, h/2)."""
    d1 = (f(x + h) - f(x - h)) / (2.0 * h)
    h2 = 0.5 * h
    d2 = (f(x + h2) - f(x - h2)) / (2.0 * h2)
    return (4.0 * d2 - d1) / 3.0


# ---------------------------------------------------------------- smoke test
def smoke():
    # e=0.01: at e<~1e-3 the endpoint-node R falls below the float64 floor of
    # E^2-V (disclosed instrument limit; grid cells are 8 orders above it)
    p, e = 100.0, 1e-2
    E, L = invariants(p, e)
    c = cycle(E, L, "smoke")
    prec = c["dphi"] - 2.0 * math.pi
    expect = 2.0 * math.pi * (1.0 / math.sqrt(1.0 - 6.0 / p) - 1.0)
    rel = abs(prec - expect) / expect
    return c, rel


# ---------------------------------------------------------------- main grid
ES = [0.1, 0.3, 0.5, 0.7, 0.9, 0.98]
# original frozen grid floor 0.05 kept; extended DOWNWARD (finer) because the
# predicted kappa* may sit below it (disclosed in dossier; no bar weakened)
KAPPAS = [0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05,
          0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0]
QS = [2.0 ** -16, 2.0 ** -20, 2.0 ** -24]
WS = [16, 20, 24]
CHANNELS = ["dphi", "dt", "dtau"]


def main():
    c_smoke, rel_smoke = smoke()
    print(f"smoke: dphi={c_smoke['dphi']:.9f} precession={c_smoke['dphi']-2*math.pi:.6e}"
          f" vs 6pi/p={(6*math.pi/100):.6e} rel={rel_smoke:.2e}")
    if rel_smoke > 5e-4:
        print("INSTRUMENT BROKEN (smoke)"); sys.exit(1)

    rows = []
    for e in ES:
        for kap in KAPPAS:
            p = 6.0 + 2.0 * e + kap
            E, L = invariants(p, e)
            C = cycle(E, L, f"e{e}/k{kap}")
            if not C["bound"]:
                rows.append({"e": e, "kappa": kap, "bound_parent": False})
                continue
            # derivatives dChannel/dE, dChannel/dL (Richardson);
            # shrink h near the separatrix until both FD arms stay bound
            def fd_cycle(hE_, hL_):
                out = {}
                for dx, dy in ((hE_, 0.0), (-hE_, 0.0), (0.0, hL_), (0.0, -hL_)):
                    cc = cycle(E + dx, L + dy, "fd")
                    if not cc["bound"]:
                        return None
                    out[(dx, dy)] = cc
                return out
            hE = hL = None
            scale = 1e-5
            while scale >= 1e-11:
                arms = fd_cycle(scale * E, scale * L)
                if arms is not None:
                    hE, hL = scale * E, scale * L
                    fdarms = arms
                    break
                scale *= 1e-2
            d = {}
            okfd = hE is not None
            for ch in CHANNELS:
                d1E = (fdarms[(hE, 0.0)][ch] - fdarms[(-hE, 0.0)][ch]) / (2.0 * hE)
                h2 = 0.5 * hE
                d2E = (cycle(E + h2, L, "fdE2")[ch] - cycle(E - h2, L, "fdE2")[ch]) / (2.0 * h2) \
                    if cycle(E + h2, L, "fdE2")["bound"] and cycle(E - h2, L, "fdE2")["bound"] else d1E
                dE_ = (4.0 * d2E - d1E) / 3.0 if d2E != d1E else d1E
                d1L = (fdarms[(0.0, hL)][ch] - fdarms[(0.0, -hL)][ch]) / (2.0 * hL)
                h2l = 0.5 * hL
                d2L = (cycle(E, L + h2l, "fdL2")[ch] - cycle(E, L - h2l, "fdL2")[ch]) / (2.0 * h2l) \
                    if cycle(E, L + h2l, "fdL2")["bound"] and cycle(E, L - h2l, "fdL2")["bound"] else d1L
                dL_ = (4.0 * d2L - d1L) / 3.0 if d2L != d1L else d1L
                if not (math.isfinite(dE_) and math.isfinite(dL_)):
                    okfd = False
                d[ch] = (dE_, dL_)
            if not okfd:
                rows.append({"e": e, "kappa": kap, "bound_parent": True,
                             "fd_failed": True})
                continue
            # kicks
            kicks = []
            for q in QS:
                for axis, idx in (("E", 0), ("L", 1)):
                    for sign in (+1.0, -1.0):
                        dE = sign * q * E if axis == "E" else 0.0
                        dL = sign * q * L if axis == "L" else 0.0
                        Ct = cycle(E + dE, L + dL, "kick")
                        taylor = {ch: C[ch] + d[ch][0] * dE + d[ch][1] * dL
                                  for ch in CHANNELS}
                        if not Ct["bound"]:
                            kicks.append({"q": q, "axis": axis, "sign": sign,
                                          "kicked_bound": False,
                                          "taylor_finite": all(
                                              math.isfinite(taylor[ch])
                                              for ch in CHANNELS)})
                            continue
                        rem = {}
                        for ch in CHANNELS:
                            r_abs = abs(taylor[ch] - Ct[ch])
                            rem[ch] = {"abs": r_abs,
                                       "budget_mult": {w: r_abs / (2.0 ** -w * abs(Ct[ch]))
                                                       for w in WS}}
                        kicks.append({"q": q, "axis": axis, "sign": sign,
                                      "kicked_bound": True,
                                      "remainder": rem})
            rows.append({"e": e, "kappa": kap, "p": p, "E": E, "L": L,
                         "bound_parent": True,
                         "cycle": {ch: C[ch] for ch in CHANNELS},
                         "derivatives": {ch: d[ch] for ch in CHANNELS},
                         "kicks": kicks})
            def worst_at(ch, q, w):
                cand = [(k["remainder"][ch]["budget_mult"][w], k["axis"])
                        for k in kicks if k.get("kicked_bound") and k["q"] == q]
                return max(cand) if cand else (float("nan"), "")
            wt = worst_at("dt", 2.0 ** -20, 20)
            wp = worst_at("dphi", 2.0 ** -20, 20)
            print(f"e={e:4} k={kap:6} h_fd={hE/E:.0e} dt={C['dt']:9.1f} "
                  f"dtR/b20={wt[0]:9.3e}({wt[1]}) phiR/b20={wp[0]:9.3e}")

    # ------------------------------------------------ summary
    def viol_band(ch, q, w):
        """smallest kappa whose row has any bound kick with budget_mult>1."""
        band = None
        for r in rows:
            if not r.get("bound_parent") or r.get("fd_failed"):
                continue
            for k in r["kicks"]:
                if k["q"] == q and k.get("kicked_bound") and \
                        k["remainder"][ch]["budget_mult"][w] > 1.0:
                    if band is None or r["kappa"] < band:
                        band = r["kappa"]
        return band

    summary = {"smoke_rel": rel_smoke,
               "kappa_star": {ch: {f"q2e{math.frexp(q)[1]}": {w: viol_band(ch, q, w)
                                                             for w in WS}
                                   for q in QS}
                              for ch in CHANNELS}}
    # q^2 scaling check on dt remainders (median ratio between q arms)
    scal = []
    for r in rows:
        if not r.get("bound_parent") or r.get("fd_failed"):
            continue
        base = {(k["axis"], k["sign"]): k for k in r["kicks"]
                if k["q"] == QS[0] and k.get("kicked_bound")}
        for key, kb in base.items():
            for q in QS[1:]:
                kk = next((x for x in r["kicks"] if x["q"] == q and
                           (x["axis"], x["sign"]) == key and x.get("kicked_bound")), None)
                if kk and base[key]["remainder"]["dt"]["abs"] > 0:
                    scal.append(kk["remainder"]["dt"]["abs"] /
                                base[key]["remainder"]["dt"]["abs"])
    if scal:
        summary["dt_remainder_ratio_q16_to_q"] = {"median": float(np.median(scal)),
                                                  "n": len(scal)}
    # crossings
    cross = [r for r in rows for k in r.get("kicks", [])
             if not k.get("kicked_bound")]
    summary["unrepresentable_kicks"] = len(cross)
    summary["unrepresentable_detail"] = [
        {"e": r["e"], "kappa": r["kappa"], "q": k["q"], "axis": k["axis"],
         "sign": k["sign"], "taylor_finite": k["taylor_finite"]}
        for r in rows for k in r.get("kicks", []) if not k.get("kicked_bound")]


    # ------------------------------------------------ analysis (regenerable)
    def row(e_, k_):
        for r in rows:
            if r["e"] == e_ and r["kappa"] == k_:
                return r
        return None

    def fails(r_, ch, q, w):
        if not r_ or not r_.get("bound_parent") or r_.get("fd_failed"):
            return None
        return any(k["q"] == q and k.get("kicked_bound")
                   and k["remainder"][ch]["budget_mult"][w] > 1.0
                   for k in r_["kicks"])

    print("\n== licensed-domain boundary (q=2^-20, w=20; largest failing kappa) ==")
    for ch in ("dt", "dphi"):
        for e_ in ES:
            kf = [r_["kappa"] for r_ in rows
                  if r_["e"] == e_ and fails(r_, ch, 2.0 ** -20, 20)]
            kp = [r_["kappa"] for r_ in rows
                  if r_["e"] == e_ and not fails(r_, ch, 2.0 ** -20, 20)
                  and r_.get("bound_parent") and not r_.get("fd_failed")]
            print(f"{ch} e={e_}: largest failing kappa={max(kf) if kf else None}"
                  f"  smallest passing={min(kp) if kp else None}")
    nviol = sum(1 for r_ in rows if fails(r_, "dt", 2.0 ** -20, 20))
    n_ok = sum(1 for r_ in rows if fails(r_, "dt", 2.0 ** -20, 20) is False)
    print(f"violating cells dt/q20/w20: {nviol}/{nviol+n_ok}")
    # worst multiples
    for ch in ("dt", "dphi"):
        w_ = max(((k["remainder"][ch]["budget_mult"][20], r_["e"], r_["kappa"])
                  for r_ in rows if r_.get("bound_parent") and not r_.get("fd_failed")
                  for k in r_["kicks"] if k.get("kicked_bound") and k["q"] == 2.0 ** -20),
                 default=(0, 0, 0))
        print(f"worst {ch} multiple @q2e-20/w20: {w_[0]:.3e} at e={w_[1]} kappa={w_[2]}")
    # axes
    ax = {}
    for r_ in rows:
        if r_.get("bound_parent") and not r_.get("fd_failed"):
            for k in r_["kicks"]:
                if k.get("kicked_bound") and k["q"] == 2.0 ** -20 \
                        and k["remainder"]["dt"]["budget_mult"][20] > 1.0:
                    ax[k["axis"]] = ax.get(k["axis"], 0) + 1
    print("violating kick axes (dt):", ax)
    # crossings by cell
    cros = {}
    for r_ in rows:
        for k in r_.get("kicks", []):
            if not k.get("kicked_bound"):
                cros.setdefault((r_["e"], r_["kappa"]), []).append(
                    (k["q"], k["axis"], k["sign"]))
    print(f"== crossings: {sum(len(v) for v in cros.values())} kicks left the bound region ==")
    for kk in sorted(cros, key=lambda z: (z[0], z[1])):
        print(f"  e={kk[0]} k={kk[1]}: {sorted(set((q, a, s) for q, a, s in cros[kk]))}")
    # ODE spot checks on violating cells
    print("== ODE spot-checks (independent path) ==")
    for (e_, k_) in [(0.5, 0.005), (0.9, 0.05)]:
        pp = 6.0 + 2.0 * e_ + k_
        E_, L_ = invariants(pp, e_)
        cq, co = cycle(E_, L_), cycle_ode(E_, L_)
        if cq["bound"] and co["bound"]:
            for ch in CHANNELS:
                print(f"e={e_} k={k_} {ch}: quad={cq[ch]:.10f} ode={co[ch]:.10f} "
                      f"rel={abs(cq[ch]-co[ch])/abs(co[ch]):.2e}")
        else:
            print(f"e={e_} k={k_}: quad_bound={cq['bound']} ode_bound={co.get('bound')}")

    json.dump({"rows": rows, "summary": summary}, open(OUT, "w"), indent=1)
    print(json.dumps(summary["kappa_star"], indent=1))
    print("unrepresentable kicks:", len(cross))
    print("q-scaling median ratio:", summary.get("dt_remainder_ratio_q16_to_q"))


if __name__ == "__main__":
    main()
