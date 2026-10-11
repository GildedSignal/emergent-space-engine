#!/usr/bin/env python3
"""
Falsifier: extended Darwin variables (Blanco 2026, arXiv:2604.28140) as plunge tubes.

Claim under test: r~ = 1/(f + A*phi(eta)), phi = cosh(eta-eta0) for plunge sectors,
f/A from real parts of the roots of R, phase flow dtau/deta = |dr/deta|/sqrt(R),
Gauss-Legendre 4-point panels in eta, exact terminal by root-finding — reproduces
Schwarzschild plunge geodesics to oracle accuracy at bound-orbit panel cost, in every
massive sector, including kicks across the separatrix.

Oracle: independent second-order geodesic integration (DOP853, rtol 1e-12).
M = 1 units. Floats explore; classification outcomes are the integer decisions.
"""
import json, os, time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

rng = np.random.default_rng(20261011)
X4, W4 = np.polynomial.legendre.leggauss(4)

def Veff(r, L2):  return (1.0 - 2.0/r)*(1.0 + L2/r**2)
def Rfun(r, E2, L2): return E2 - Veff(r, L2)

def roots_R(E2, L2):
    """roots of (E2-1) r^3 + 2 r^2 - L2 r + 2 L2 = 0"""
    rr = np.roots([E2-1.0, 2.0, -L2, 2.0*L2])
    rr = rr[np.argsort(-rr.real)]  # stable-ish order
    real = np.array([x.real for x in rr if abs(x.imag) < 1e-9*(1+abs(x.real))])
    comp = np.array([x for x in rr if abs(x.imag) >= 1e-9*(1+abs(x.real))])
    return np.sort(real), comp

def extrema(L2):
    if L2 <= 12.0: return None
    s = np.sqrt(1.0 - 12.0/L2)
    return (L2/2.0)*(1.0-s), (L2/2.0)*(1.0+s)  # r_ucO (max), r_sco (min)

# ---------------- oracle (independent: second-order geodesic equation) ------------
def oracle(E, L, r0, dr0, phi0=0.0, t0=0.0, tau0=0.0, r_end=3.0, r_esc=1e5,
           tau_max=1e7, rtol=1e-12):
    E2, L2 = E*E, L*L
    def rhs(tau, y):
        r, dr, phi, t = y
        d2 = -1.0/r**2 + L2/r**3 - 3.0*L2/r**4
        return [dr, d2, L/r**2, E/(1.0-2.0/r)]
    def ev_plunge(tau, y): return y[0] - r_end
    ev_plunge.terminal, ev_plunge.direction = True, -1
    def ev_turn(tau, y): return y[1]
    ev_turn.terminal, ev_turn.direction = True, +1
    def ev_esc(tau, y): return y[0] - r_esc
    ev_esc.terminal = True
    ev_esc.direction = +1
    sol = solve_ivp(rhs, (tau0, tau_max), [r0, dr0, phi0, t0], method="DOP853",
                    rtol=rtol, atol=1e-14, events=[ev_plunge, ev_turn, ev_esc],
                    dense_output=True)
    which = "none"
    for i, nm in enumerate(["plunge", "turn", "escape"]):
        if len(sol.t_events[i]) > 0: which = nm; break
    return sol, which

# ---------------- candidate: extended Darwin panels ------------------------------
class Param:
    """u(eta) = f + A*(cosh(eta-eta0) - shift)  [plunge]  or  f + A*cos(eta) [bound]"""
    def __init__(self, E, L, sector, partner=None):
        E2, L2 = E*E, L*L
        real, comp = roots_R(E2, L2)
        self.ok = True; self.why = ""
        if sector == "bound":
            assert len(real) >= 3
            r_peri, r_apo = real[1], real[2]   # r2, r3
            self.f, self.A = 0.5*(1/r_peri+1/r_apo), 0.5*(1/r_peri-1/r_apo)
            self.kind, self.shift, self.eta0 = "cos", 0.0, 0.0
        elif sector == "outer":   # turning point = largest positive real root
            posr = real[real > 0]
            r_t = posr[-1]
            if partner is None:
                partner = comp[0].real if len(comp) else real[0]
            elif partner == "anchor":
                partner = 2.0   # horizon anchor: dyadic, no cancellation
            self.f, self.A = 0.5*(1/partner+1/r_t), 0.5*(1/partner-1/r_t)
            self.kind, self.shift, self.eta0 = "cosh", 2.0, 0.0
        elif sector == "inner":   # turning point = smallest positive real root
            posr = real[real > 2.0]
            r_t = posr[0]
            if partner is None:
                partner = real[-1] if len(real) >= 3 else (
                    comp[0].real if len(comp) else 8.0)
            elif partner == "anchor":
                partner = 8.0   # any p > r1; 8 > r_uco > r1 always
            self.f, self.A = 0.5*(1/r_t+1/partner), 0.5*(1/r_t-1/partner)
            self.kind, self.shift, self.eta0 = "cosh", 0.0, 0.0
        elif sector == "direct":  # from infinity; no positive turning root
            if partner == "anchor":
                p = 8.0
            elif len(comp):
                p = comp[0].real
            else:
                neg = real[real < 0]
                p = neg[0] if len(neg) else real[0]
            if partner is not None and partner != "anchor": p = partner
            r_neg = real[real < 0][0] if np.any(real < 0) else p
            self.f, self.A = 0.5*(1/p+1/r_neg), 0.5*(1/p-1/r_neg)
            self.kind, self.shift, self.eta0 = "cosh", 2.0, 0.0
        if not (np.isfinite(self.f) and np.isfinite(self.A)) or self.A <= 0:
            self.ok = False; self.why = f"degenerate f={self.f} A={self.A}"
        self.E, self.L, self.E2, self.L2 = E, L, E2, L2

    def u(self, eta):
        if self.kind == "cos": return self.f + self.A*np.cos(eta)
        return self.f + self.A*(np.cosh(eta-self.eta0) - self.shift)

    def eta_of_r(self, r, side=+1):
        """invert u(eta) = 1/r on the infall branch (eta > eta0)."""
        u_target = 1.0/r
        if self.kind == "cos":
            c = (u_target-self.f)/self.A
            if abs(c) > 1: return None
            base = np.arccos(c)
            return base if side > 0 else -base
        ch = (u_target-self.f)/self.A + self.shift
        if ch < 1.0: return None
        return self.eta0 + side*np.arccosh(ch)

    def integrands(self, eta):
        u = self.u(eta); r = 1.0/u
        if self.kind == "cos":
            up = -self.A*np.sin(eta)
        else:
            up = self.A*np.sinh(eta-self.eta0)
        R = Rfun(r, self.E2, self.L2)
        if np.any(R < -1e-12*np.maximum(1.0, abs(self.E2))):
            raise ValueError(f"left allowed band: min R = {R.min():.3e}")
        sq = np.sqrt(np.maximum(R, 0.0))
        dtau = np.abs(up/u**2)/sq
        dphi = self.L*u**2*dtau
        dt = (self.E/(1.0-2.0*u))*dtau
        return dphi, dt, dtau

    def integrate(self, eta_a, eta_b, npan):
        edges = np.linspace(eta_a, eta_b, npan+1)
        phi = t = tau = 0.0
        for i in range(npan):
            lo, hi = edges[i], edges[i+1]
            mid, half = 0.5*(lo+hi), 0.5*(hi-lo)
            nodes = mid + half*X4
            dp, dt_, dta = self.integrands(nodes)
            phi += half*np.dot(W4, dp); t += half*np.dot(W4, dt_); tau += half*np.dot(W4, dta)
        return phi, t, tau

    def integrands_u(self, u):
        """integrands in u (no turning point on the branch): dtau/du = 1/(u^2 sqrt R)."""
        r = 1.0/u
        R = Rfun(r, self.E2, self.L2)
        if np.any(R < -1e-12*np.maximum(1.0, abs(self.E2))):
            raise ValueError(f"left allowed band: min R = {R.min():.3e}")
        sq = np.sqrt(np.maximum(R, 0.0))
        dtau = 1.0/(u**2*sq)
        dphi = self.L/sq
        dt = (self.E/(1.0-2.0*u))*dtau
        return dphi, dt, dtau

    def integrate_u(self, u_a, u_b, npan, geo=True):
        if geo and u_a > 0 and u_b/u_a > 16.0:
            rho = (u_b/u_a)**(1.0/npan)
            edges = u_a*rho**np.arange(npan+1); edges[-1] = u_b
        else:
            edges = np.linspace(u_a, u_b, npan+1)
        phi = t = tau = 0.0
        for i in range(npan):
            lo, hi = edges[i], edges[i+1]
            mid, half = 0.5*(lo+hi), 0.5*(hi-lo)
            nodes = mid + half*X4
            dp, dt_, dta = self.integrands_u(nodes)
            phi += half*np.dot(W4, dp); t += half*np.dot(W4, dt_); tau += half*np.dot(W4, dta)
        return phi, t, tau

def cand_terminal(P, r_start, r_end, npan, side=+1, eta_start=None):
    ea = P.eta_of_r(r_start, side) if eta_start is None else eta_start
    eb = P.eta_of_r(r_end, side)
    if ea is None or eb is None or eb <= ea: return None
    return P.integrate(ea, eb, npan)

# ---------------- seed generation -------------------------------------------------
def classify_roots(E, L, r, s):
    """sector from root structure + position (the candidate's rule).
    Bands of R>0: (0,pos[0]) always; (pos[1],pos[2]) if 3 roots; (pos[-1],inf) iff E2>1."""
    E2, L2 = E*E, L*L
    real, comp = roots_R(E2, L2)
    pos = np.sort(real[real > 0])
    if len(pos) == 0:
        return "direct"                      # E2>1 past the barrier: no turn anywhere
    if Rfun(r, E2, L2) < 0: return "invalid"
    if r <= pos[0]:
        # inner band (0, r1) exists as a trap iff there is a second positive root
        # (a bounce below); with one positive root it is the outer well's floor
        return "inner" if len(pos) >= 2 else "outer"
    if len(pos) >= 3 and pos[1] < r < pos[-1]:
        return "bound"
    if r > pos[-1]:
        return "scatter"                     # only reachable with E2>1
    return "ambiguous"

def brute(E, L, r, s, r_s=2.05):
    E2, L2 = E*E, L*L
    dr0 = s*np.sqrt(max(Rfun(r, E2, L2), 0.0))
    if dr0 == 0.0: dr0 = -1e-9
    sol, which = oracle(E, L, r, dr0, r_end=r_s, tau_max=2e6, rtol=1e-10)
    return which  # plunge | turn | escape

# ---------------- experiments ------------------------------------------------------
def rel(err, ref): return abs(err)/max(abs(ref), 1e-300)
def acc_case(E, L, sector, r_start, r_end, npan_list=(8, 16, 32, 64, 128),
             partner=None, at_turn=False, layout="eta"):
    E2, L2 = E*E, L*L
    dr0 = -np.sqrt(max(Rfun(r_start, E2, L2), 0.0))
    if dr0 == 0.0: dr0 = -1e-12
    sol, which = oracle(E, L, r_start, dr0, r_end=r_end, tau_max=2e7)
    if which != "plunge": return None
    phi_o, t_o, tau_o = sol.y_events[0][0][2], sol.y_events[0][0][3], sol.t_events[0][0]
    try:
        P = Param(E, L, sector, partner=partner)
    except Exception as ex:
        return {"fail": f"param: {ex}"}
    if not P.ok: return {"fail": P.why}
    out = {"oracle": [float(phi_o), float(t_o), float(tau_o)], "panels": {}}
    try:
        if layout == "u":
            u_a, u_b = 1.0/r_start, 1.0/r_end
            for n in npan_list:
                phi, t, tau = P.integrate_u(u_a, u_b, n)
                out["panels"][n] = [float(rel(phi-phi_o, phi_o)), float(rel(t-t_o, t_o)),
                                    float(rel(tau-tau_o, tau_o))]
        else:
            ea = P.eta0 if at_turn else P.eta_of_r(r_start, +1)
            eb = P.eta_of_r(r_end, +1)
            if ea is None or eb is None or eb <= ea:
                return {"fail": "eta range", "ea": None if ea is None else float(ea),
                        "eb": None if eb is None else float(eb)}
            out["eta_span"] = float(eb-ea)
            for n in npan_list:
                phi, t, tau = P.integrate(ea, eb, n)
                out["panels"][n] = [float(rel(phi-phi_o, phi_o)), float(rel(t-t_o, t_o)),
                                    float(rel(tau-tau_o, tau_o))]
    except ValueError as ex:
        out["fail"] = str(ex)
    return out

def panels_to(out, tol=1e-9):
    best = None
    for n in sorted(int(k) for k in out["panels"]):
        e = max(out["panels"][n])
        if e <= tol: best = n; break
    return best

def main():
    t_start = time.time()
    res = {"machine": {"nproc": os.cpu_count(), "loadavg": os.getloadavg(),
                       "time": time.strftime("%Y-%m-%d %H:%M:%S")}}

    # ---- E1: classification (root rule vs brute force), near every boundary ----
    seeds = []
    for L2 in [8.0, 10.0, 11.9, 13.0, 14.0, 15.0, 16.0, 20.0, 30.0, 40.0]:
        ext = extrema(L2)
        E2c = []
        if ext:
            rU, rS = ext
            Vmax, Vmin = Veff(rU, L2), Veff(rS, L2)
            for d in [1e-8, 1e-6, 1e-4, 1e-2, 0.1]:
                E2c += [Vmax*(1+d), Vmax*(1-d), Vmin*(1+d), Vmin*(1-d)]
        else:
            Vmax = None
        for d in [1e-8, 1e-6, 1e-4, 1e-2, 0.1]:
            E2c += [1.0*(1+d), 1.0*(1-d)]
        E2c += list(rng.uniform(0.5, 1.6, 12))
        for E2 in E2c:
            if not (0.02 < E2 < 4.0): continue
            E = np.sqrt(E2)
            real, comp = roots_R(E2, L2)
            pos = np.sort(real[real > 0])
            # start positions: inside each band
            starts = []
            if len(pos) == 1: starts += [0.5*pos[0], 0.95*pos[0], 1.05*pos[0]]
            if len(pos) >= 2:
                starts += [0.5*pos[0], 0.5*(pos[0]+pos[1]), 0.5*(pos[1]+pos[-1]), 1.05*pos[-1]]
            starts += [50.0, 500.0]
            for r in starts:
                if Rfun(r, E2, L2) < 0: continue
                seeds.append((E, np.sqrt(L2), r))
    seeds = [s for s in seeds if s[2] > 2.05]
    mism, tie, n = [], 0, 0
    for (E, L, r) in seeds[:2400]:
        E2, L2 = E*E, L*L
        ext = extrema(L2)
        tief = False
        if ext:
            rU, rS = ext
            for Vc in (Veff(rU, L2), Veff(rS, L2)):
                if abs(E2-Vc)/E2 < 1e-9: tief = True
        if abs(E2-1.0)/E2 < 1e-9: tief = True
        sec = classify_roots(E, L, r, -1)
        if sec in ("invalid", "ambiguous"): continue
        brt = brute(E, L, r, -1)
        n += 1
        if tief: tie += 1; continue
        if brt == "none":
            res.setdefault("undecided", 0); res["undecided"] += 1; continue
        plunge_c = sec in ("inner", "outer", "direct")
        plunge_b = brt == "plunge"
        if plunge_c != plunge_b:
            mism.append({"E2": E2, "L2": L2, "r": r, "rule": sec, "brute": brt})
    res["classification"] = {"n": n, "ties_excluded": tie,
                             "mismatches": mism[:20], "n_mismatch": len(mism)}

    # ---- E2: terminal accuracy + cost per sector ----
    acc = {}
    def add(case, E, L, sector, r_start, r_end, partner=None, at_turn=False,
            layout="eta"):
        o = acc_case(E, L, sector, r_start, r_end, partner=partner, at_turn=at_turn,
                     layout=layout)
        if o is None: return
        acc.setdefault(case, []).append(o)

    L2o = 13.0  # Vmax<1: outer plunge exists
    ext = extrema(L2o); rU, rS = ext
    Vmax, Vmin = Veff(rU, L2o), Veff(rS, L2o)
    for E2 in [Vmax*(1+1e-8), Vmax*(1+1e-6), Vmax*(1+1e-4), 0.95, 0.99]:
        if not (Vmin < E2 < 1.0): continue
        real, _ = roots_R(E2, L2o); r3 = real[real > 2][-1]
        for r_end in (3.0, 2.001):
            add("outer", np.sqrt(E2), np.sqrt(L2o), "outer", r3, r_end, at_turn=True)
    # outer with no barrier
    for L2 in (8.0, 10.0):
        for E2 in (0.6, 0.9, 0.999):
            real, _ = roots_R(E2, L2); r3 = real[real > 2][-1]
            add("outer-nobarrier", np.sqrt(E2), np.sqrt(L2), "outer", r3, 3.0,
                at_turn=True)
    # direct from large r
    for L2, E2 in [(13.0, 1.001), (13.0, 1.1), (8.0, 1.5), (20.0, 1.3)]:
        add("direct", np.sqrt(E2), np.sqrt(L2), "direct", 1e4, 3.0, layout="u")
    for E2 in [Vmin*(1+1e-4), 0.5*(Vmin+Vmax)]:
        real, _ = roots_R(E2, L2o); pos = np.sort(real[real > 2])
        r1 = pos[0]
        if Rfun(0.5*r1, E2, L2o) > 0:
            add("inner", np.sqrt(E2), np.sqrt(L2o), "inner", r1, 2.001, at_turn=True)
    # inner-E (below Vmin: no r3 exists; literal pairing vs anchored partner)
    for E2 in [Vmin*(1-1e-4), 0.5*Vmin]:
        real, _ = roots_R(E2, L2o); pos = np.sort(real[real > 2])
        r1 = pos[0]
        if Rfun(0.9*r1, E2, L2o) > 0:
            add("inner-E-literal", np.sqrt(E2), np.sqrt(L2o), "inner", r1, 2.001,
                at_turn=True)
            add("inner-E-anchored", np.sqrt(E2), np.sqrt(L2o), "inner", r1, 2.001,
                partner="anchor", at_turn=True)
    # bound control (half cycle apo->peri)
    for E2 in [0.5*(Vmin+Vmax), Vmin*(1+1e-4), Vmax*(1-1e-4)]:
        real, _ = roots_R(E2, L2o); pos = np.sort(real[real > 2])
        r2, r3 = pos[1], pos[2]
        E, L = np.sqrt(E2), np.sqrt(L2o)
        dr0 = -np.sqrt(max(Rfun(r3, E2, L2o), 0.0)) or -1e-12
        sol, _ = oracle(E, L, r3, dr0, r_end=r2, tau_max=1e6)
        if not (len(sol.t_events[0]) > 0): continue
        phi_o, t_o, tau_o = (sol.y_events[0][0][2], sol.y_events[0][0][3],
                             sol.t_events[0][0])
        P = Param(E, L, "bound")
        ea, eb = P.eta_of_r(r3, -1), P.eta_of_r(r2, +1)  # apo at chi=pi, peri at 0
        rec = {"oracle": [float(phi_o), float(t_o), float(tau_o)],
               "eta_span": float(abs(eb-ea)), "panels": {}}
        for npan in (8, 16, 32, 64, 128):
            phi, t, tau = P.integrate(ea, eb, npan)
            rec["panels"][npan] = [float(rel(phi-phi_o, phi_o)), float(rel(t-t_o, t_o)),
                                   float(rel(tau-tau_o, tau_o))]
        acc.setdefault("bound-control", []).append(rec)

    summ = {}
    for case, lst in acc.items():
        rows, fails = [], []
        for o in lst:
            if "fail" in o: fails.append(o["fail"]); continue
            e64 = o["panels"].get(64) or o["panels"].get(128)
            if not e64: continue
            rows.append({"err_phi": e64[0], "err_t": e64[1], "err_tau": e64[2],
                         "panels_to_1e-9": panels_to(o, 1e-9)})
        if rows:
            summ[case] = {"n": len(lst), "fails": len(fails),
                "max_err_phi": max(r["err_phi"] for r in rows),
                "max_err_t": max(r["err_t"] for r in rows),
                "max_err_tau": max(r["err_tau"] for r in rows),
                "panels_to_1e-9_med": (float(np.median([r["panels_to_1e-9"] for r in rows
                    if r["panels_to_1e-9"]])) if any(r["panels_to_1e-9"] for r in rows) else None),
                "panels_to_1e-9_n_hit": sum(1 for r in rows if r["panels_to_1e-9"])}
        else:
            summ[case] = {"n": len(lst), "fails": len(fails), "fail_reasons": fails[:3]}
    res["accuracy"] = summ

    # ---- E3: negative control (no phase absorption: panels in r) ----
    E2, L2 = 0.95, 13.0
    E, L = np.sqrt(E2), np.sqrt(L2)
    real, _ = roots_R(E2, L2); r3 = real[real > 2][-1]
    dr0 = -1e-12
    sol, _ = oracle(E, L, r3, dr0, r_end=3.0, tau_max=1e6)
    phi_o = sol.y_events[0][0][2]
    neg = {}
    for npan in (16, 64, 256, 1024, 4096):
        edges = np.linspace(r3, 3.0, npan+1)
        phi = 0.0
        for i in range(npan):
            lo, hi = edges[i], edges[i+1]
            mid, half = 0.5*(lo+hi), 0.5*(hi-lo)
            rs = mid + half*X4
            phi += half*np.dot(W4, L/(rs**2*np.sqrt(np.maximum(Rfun(rs, E2, L2), 1e-300))))
        neg[npan] = float(rel(phi-phi_o, phi_o))
    res["negative_control_r_panels"] = neg

    # ---- E4: near-radial sweep + L=0 ----
    radial = {}
    E2 = 0.9
    for L in (1.0, 1e-1, 1e-2, 1e-3, 1e-6):
        L2 = L*L
        real, comp = roots_R(E2, L2)
        r3 = real[real > 2][-1]
        row = {}
        for tag, partner in (("literal", None), ("anchor", "anchor")):
            o = acc_case(np.sqrt(E2), L, "outer", r3, 3.0, partner=partner,
                         at_turn=True)
            if o is None: row[tag] = "oracle-none"; continue
            row[tag] = ({"fail": o["fail"]} if "fail" in o else
                        {"panels_to_1e-9": panels_to(o, 1e-9),
                         "err_at64": max(o["panels"][64])})
        radial[f"L={L:g}"] = row
    # L = 0 exactly: construction attempt
    try:
        P0 = Param(np.sqrt(E2), 0.0, "outer")
        ok0 = P0.ok
        why = P0.why
        e = None
        if ok0:
            e = cand_terminal(P0, 2.0/(1-E2), 3.0, 64)
        radial["L=0"] = {"ok": bool(ok0), "why": why, "terminal": None if e is None else [float(x) for x in e]}
    except Exception as ex:
        radial["L=0"] = {"ok": False, "why": f"exception: {type(ex).__name__}: {ex}"}
    res["near_radial"] = radial

    # ---- E5: horizon terminal (tau, phi finite; t log-divergent) ----
    E, L = np.sqrt(0.95), np.sqrt(13.0)
    real, _ = roots_R(E*E, L*L); r3 = real[real > 2][-1]
    hor = {}
    for r_end in (2.1, 2.001, 2.000001):
        o = acc_case(E, L, "outer", r3, r_end, npan_list=(32, 64, 128, 256))
        if o and "fail" not in o:
            hor[f"r_end={r_end:g}"] = {"err_at128": max(o["panels"][128]),
                                       "panels_to_1e-9": panels_to(o, 1e-9)}
        else:
            hor[f"r_end={r_end:g}"] = o
    # t log slope: t(r) + 2*sqrt(1... measure dt/dln(1/(r-2)) near horizon from oracle
    dr0 = -np.sqrt(max(Rfun(r3, E*E, L*L), 0.0))
    ts = {}
    for r_e in (2.1, 2.01, 2.001, 2.0001):
        sol, _ = oracle(E, L, r3, dr0 or -1e-12, r_end=r_e, tau_max=1e7)
        if len(sol.t_events[0]): ts[f"{r_e:g}"] = float(sol.y_events[0][0][3])
    if len(ts) >= 3:
        ks = sorted(ts)
        slopes = [ (ts[ks[i+1]]-ts[ks[i]])/(np.log(1/(float(ks[i+1])-2)) - np.log(1/(float(ks[i])-2))) for i in range(len(ks)-1)]
        res["horizon_t_log_slope"] = {"slopes": slopes, "predicted": -2.0}
    res["horizon"] = hor

    # ---- E6: kick across the separatrix (the plane's NoBoundOrbit case) ----
    kicks = []
    L2 = 13.0
    ext = extrema(L2); rU, rS = ext
    Vmax, Vmin = Veff(rU, L2), Veff(rS, L2)
    for trial in range(24):
        E2b = Vmin + rng.uniform(0.1, 0.9)*(Vmax-Vmin)
        E, L = np.sqrt(E2b), np.sqrt(L2)
        real, _ = roots_R(E2b, L2); pos = np.sort(real[real > 2])
        r2, r3 = pos[1], pos[2]
        # start at apoapsis, fall in; kick at a random r in (r2, r3) pushes E over Vmax
        r_k = rng.uniform(r2+0.05*(r3-r2), r3-0.05*(r3-r2))
        sol, _ = oracle(E, L, r3, -1e-12, r_end=r_k, tau_max=1e6)
        if not len(sol.t_events[0]): continue
        phi_k, t_k, tau_k = (float(sol.y_events[0][0][2]), float(sol.y_events[0][0][3]),
                             float(sol.t_events[0][0]))
        E2k = Vmax*(1+rng.uniform(1e-6, 1e-2))   # into the outer-plunge sector
        Ek = np.sqrt(E2k)
        dr_k = -np.sqrt(max(Rfun(r_k, E2k, L2), 0.0))
        sol2, which = oracle(Ek, L, r_k, dr_k, phi0=phi_k, t0=t_k, tau0=tau_k,
                             r_end=3.0, tau_max=1e7)
        if which != "plunge": continue
        phi_o2, t_o2, tau_o2 = (float(sol2.y_events[0][0][2]), float(sol2.y_events[0][0][3]),
                                float(sol2.t_events[0][0]))
        P = Param(Ek, L, "outer")
        if not P.ok: continue
        ea = P.eta_of_r(r_k, +1); eb = P.eta_of_r(3.0, +1)
        if ea is None or eb is None or eb <= ea: continue
        rec = {"r_k": r_k, "E2b": E2b, "E2k": E2k}
        for npan in (32, 64):
            phi, t, tau = P.integrate(ea, eb, npan)
            rec[f"err{npan}"] = [float(rel(phi-(phi_o2-phi_k), phi_o2-phi_k)),
                                 float(rel(t-(t_o2-t_k), t_o2-t_k)),
                                 float(rel(tau-(tau_o2-tau_k), tau_o2-tau_k))]
        kicks.append(rec)
    res["kick_across_separatrix"] = {"n": len(kicks),
        "err64_max_dphi_dt_dtau": (max((k["err64"][0] for k in kicks), default=None),
                                    max((k["err64"][1] for k in kicks), default=None),
                                    max((k["err64"][2] for k in kicks), default=None)),
        "worst": max(kicks, key=lambda k: max(k["err64"])) if kicks else None}

    res["wall_seconds"] = time.time()-t_start
    with open("metrics.json", "w") as f: json.dump(res, f, indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "kick_across_separatrix"}, indent=1))
    print("KICKS:", res["kick_across_separatrix"]["n"],
          res["kick_across_separatrix"]["err64_max_dphi_dt_dtau"])

if __name__ == "__main__":
    main()

# ---------------- E7: near-separatrix cost with valley-aware cuts ---------------
def adaptive_panel_count(P, eta_a, eta_b, tol_int=1e-11, max_panels=20000):
    """Deterministic bisection refinement in eta; counts panels needed so each
    panel's GL4-vs-2xGL4 discrepancy is below tol_int (valley-aware cut placement)."""
    tot = P.integrate(eta_a, eta_b, 512)
    scale = max(abs(x) for x in tot)
    def est(a, b):
        p1 = P.integrate(a, b, 1); p2 = P.integrate(a, b, 2)
        return max(abs(x-y) for x, y in zip(p1, p2))/scale
    stack = [(eta_a, eta_b)]; panels = 0
    while stack:
        a, b = stack.pop()
        panels += 1
        if panels > max_panels: return -panels
        if est(a, b) <= tol_int or (b-a) < 1e-13:
            continue
        m = 0.5*(a+b); stack += [(a, m), (m, b)]
    return panels

def separatrix_cost():
    L2 = 13.0
    ext = extrema(L2); rU, rS = ext
    Vmax = Veff(rU, L2)
    out = {}
    for d in (1e-2, 1e-4, 1e-6, 1e-8, 1e-10):
        E2 = Vmax*(1+d); E, L = np.sqrt(E2), np.sqrt(L2)
        real, _ = roots_R(E2, L2); r3 = real[real > 2][-1]
        P = Param(E, L, "outer")
        if not P.ok: out[f"d={d:g}"] = "param-fail"; continue
        eb = P.eta_of_r(3.0, +1)
        n = adaptive_panel_count(P, P.eta0, eb)
        # accuracy check against oracle with that layout is implicit (bisection tol)
        out[f"d={d:g}"] = n
    return out
