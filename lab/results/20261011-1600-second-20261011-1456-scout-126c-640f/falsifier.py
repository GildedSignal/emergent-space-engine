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
        self.real_roots, self.comp_roots = real, comp
        # TRAP for the b-plunge-tubes builder (checker, 11 Oct): on the cos
        # branch side=+1 returns arccos in [0, pi], i.e. the OUTGOING half
        # (periapsis at eta=0, apoapsis at eta=pi); side=-1 is inbound. The
        # cosh branch is single-covered: side selects the infall (eta>eta0)
        # vs outgoing branch. eta_of_r returns None outside the band.
        self.E, self.L, self.E2, self.L2 = E, L, E2, L2
        self.real_roots, self.comp_roots = real, comp

    def u(self, eta):
        if self.kind == "cos": return self.f + self.A*np.cos(eta)
        return self.f + self.A*(np.cosh(eta-self.eta0) - self.shift)

    def eta_of_r(self, r, side=+1):
        """invert u(eta) = 1/r on the infall branch (eta > eta0)."""
        u_target = 1.0/r
        if self.kind == "cos":
            c = (u_target-self.f)/self.A
            if c < -1.0:
                if c < -1.0-1e-9: return None
                c = -1.0   # clamp: apoapsis/periapsis roots are exact in
                           # exact arithmetic; float rounds just outside
            elif c > 1.0:
                if c > 1.0+1e-9: return None
                c = 1.0
            base = np.arccos(c)
            return base if side > 0 else -base
        ch = (u_target-self.f)/self.A + self.shift
        if ch < 1.0: return None
        return self.eta0 + side*np.arccosh(ch)

    def Rfact(self, r):
        """R in the law's own form: factored by the roots of the radial cubic,
        R*r^3 = (E2-1)*prod(r - root). The complex pair enters as
        (r-a)^2 + b^2, so near a valley bottom (R ~ delta*Vmax) there is no
        cancellation; Rfun = E2 - Veff loses ~eps/delta relative there."""
        r = np.asarray(r, dtype=float)
        val = np.full(r.shape, self.E2-1.0)
        for x in self.real_roots:
            val = val*(r-x)
        for z in self.comp_roots:
            if z.imag <= 0: continue   # conjugate pairs: take each once
            val = val*((r-z.real)**2 + z.imag**2)
        return val/r**3

    def integrands(self, eta, rform="fun"):
        u = self.u(eta); r = 1.0/u
        if self.kind == "cos":
            up = -self.A*np.sin(eta)
        else:
            up = self.A*np.sinh(eta-self.eta0)
        R = Rfun(r, self.E2, self.L2) if rform == "fun" else self.Rfact(r)
        if np.any(R < -1e-12*np.maximum(1.0, abs(self.E2))):
            raise ValueError(f"left allowed band: min R = {R.min():.3e}")
        sq = np.sqrt(np.maximum(R, 0.0))
        dtau = np.abs(up/u**2)/sq
        dphi = self.L*u**2*dtau
        dt = (self.E/(1.0-2.0*u))*dtau
        return dphi, dt, dtau

    def integrate_edges(self, edges, rform="fun"):
        """GL4 panels over an explicit edge array (the law's cut layout)."""
        phi = t = tau = 0.0
        for i in range(len(edges)-1):
            lo, hi = edges[i], edges[i+1]
            mid, half = 0.5*(lo+hi), 0.5*(hi-lo)
            nodes = mid + half*X4
            dp, dt_, dta = self.integrands(nodes, rform)
            phi += half*np.dot(W4, dp); t += half*np.dot(W4, dt_); tau += half*np.dot(W4, dta)
        return phi, t, tau

    def integrate(self, eta_a, eta_b, npan):
        edges = np.linspace(eta_a, eta_b, npan+1)
        return self.integrate_edges(edges)

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

# ---------------- the law's fixed valley cuts (integer bands) ----------------------
def valley_sigma(P):
    """Distance from the real-eta axis to the nearest complex-eta branch point
    of the phase flow: the image of the complex root pair of the radial cubic
    under eta <- arccosh((1/root - f)/A + shift). A FIXED function of (E, L):
    the same root structure the classification uses, no integrand probing.
    Near the separatrix sigma ~ C*sqrt(delta), delta = (E2-Vmax)/E2."""
    if P.kind != "cosh" or not len(P.comp_roots): return None
    sig = None
    for z in P.comp_roots:
        ch = (1.0/z - P.f)/P.A + P.shift
        e = np.arccosh(complex(ch))
        s = abs(e.imag)
        if sig is None or s < sig: sig = s
    return sig

def ladder_edges(P, eta_a, eta_b, n_base=32, safety=2.0, m=1):
    """The compiler's own cut layout for a valley: a uniform base of n_base
    panels plus dyadic rungs toward the barrier top eta(r_U) (the critical
    radius where V_eff' = 0, i.e. the real part the complex pair collapses to
    at the separatrix), down to finest width sigma/safety. B9's pattern —
    geometric bands 2^(k/m), here m = 1 per octave of distance-to-barrier-top,
    as cuts in the phase. Fixed function of (E, L); degenerates to the uniform
    base when there is no valley (sigma >= h0) or no barrier crossing."""
    n0 = max(4, int(n_base))
    base = np.linspace(eta_a, eta_b, n0+1)
    meta = {"layout": "uniform", "eta_U": None, "sigma": None, "J": 0}
    ext = extrema(P.L2)
    if P.kind != "cosh" or ext is None:
        return base, meta
    rU, _ = ext
    uU = 1.0/rU
    ua, ub = P.u(eta_a), P.u(eta_b)
    if not (min(ua, ub) < uU < max(ua, ub)):
        return base, meta          # the branch never crosses the barrier top
    eta_U = P.eta_of_r(rU, +1)
    if eta_U is None or not (eta_a < eta_U < eta_b):
        return base, meta
    sig = valley_sigma(P)
    if sig is None:
        return base, meta
    h0 = (eta_b-eta_a)/n0
    w = sig/safety
    meta.update({"eta_U": float(eta_U), "sigma": float(sig)})
    if w >= h0:
        return base, meta          # valley resolved by the base already
    J = m*int(np.ceil(np.log2(h0/w)))
    rungs = [eta_U]
    for j in range(J+1):
        for s in (+1.0, -1.0):
            x = eta_U + s*h0*2.0**(-j/m)
            if eta_a < x < eta_b: rungs.append(x)
    allr = sorted(base.tolist() + rungs)
    tol = 1e-12*(eta_b-eta_a)
    merged = [allr[0]]
    for x in allr[1:]:
        if x - merged[-1] > tol: merged.append(x)
    merged[0], merged[-1] = eta_a, eta_b
    meta.update({"layout": "ladder", "J": J})
    return np.array(merged), meta

def valley_acc(E, L, sector, r_start, r_end, at_turn=False, n_base=32,
               safety=2.0, npan_list=(32, 64)):
    """Terminal accuracy of the FIXED ladder layout vs the oracle, both R-forms,
    plus the uniform-panel baseline; oracle first-integral violation recorded
    as the truth certificate."""
    E2, L2 = E*E, L*L
    dr0 = -np.sqrt(max(Rfun(r_start, E2, L2), 0.0))
    if dr0 == 0.0: dr0 = -1e-12
    sol, which = oracle(E, L, r_start, dr0, r_end=r_end, tau_max=2e7)
    if which != "plunge" or not len(sol.t_events[0]): return None
    phi_o = float(sol.y_events[0][0][2]); t_o = float(sol.y_events[0][0][3])
    tau_o = float(sol.t_events[0][0])
    ts = np.linspace(0.0, tau_o, 2000)
    ys = sol.sol(ts)
    viol = float(np.max(np.abs(ys[1]**2 + Veff(ys[0], L2) - E2)/E2))
    try:
        P = Param(E, L, sector)
    except Exception as ex:
        return {"fail": f"param: {ex}"}
    if not P.ok: return {"fail": P.why}
    ea = P.eta0 if at_turn else P.eta_of_r(r_start, +1)
    eb = P.eta_of_r(r_end, +1)
    if ea is None or eb is None or eb <= ea:
        return {"fail": "eta range"}
    out = {"oracle": [phi_o, t_o, tau_o], "oracle_viol": viol,
           "eta_span": float(eb-ea), "uniform": {}, "ladder": {}}
    for n in npan_list:
        phi, t, tau = P.integrate(ea, eb, n)
        out["uniform"][str(n)] = [float(rel(phi-phi_o, phi_o)), float(rel(t-t_o, t_o)),
                                  float(rel(tau-tau_o, tau_o))]
    edges, meta = ladder_edges(P, ea, eb, n_base=n_base, safety=safety)
    for rform in ("fun", "factored"):
        try:
            phi, t, tau = P.integrate_edges(edges, rform)
            out["ladder"][rform] = {"panels": int(len(edges)-1),
                "err": [float(rel(phi-phi_o, phi_o)), float(rel(t-t_o, t_o)),
                        float(rel(tau-tau_o, tau_o))]}
        except ValueError as ex:
            out["ladder"][rform] = {"panels": int(len(edges)-1), "fail": str(ex)}
    m = dict(meta); m["panels"] = int(len(edges)-1)
    out["ladder_meta"] = m
    return out

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
    # bound control (half cycle apo->peri), now a live path. The pre-11-Oct
    # block ended the oracle at r_end = r2: near periapsis r(tau) is
    # quadratic, so the dip below any r_end marginally above r2 lasts less
    # than one DOP853 step, the direction-filtered plunge event never sees a
    # sign change, and every seed silently `continue`d (dead code). The live
    # path ends the oracle at its turn event and then matches both sides at
    # the exact root r2 (see below).
    bc = {}
    for E2 in [0.5*(Vmin+Vmax), Vmin*(1+1e-4), Vmax*(1-1e-4)]:
        real, _ = roots_R(E2, L2o); pos = np.sort(real[real > 2])
        r2, r3 = pos[1], pos[2]
        E, L = np.sqrt(E2), np.sqrt(L2o)
        dr0 = -np.sqrt(max(Rfun(r3, E2, L2o), 0.0)) or -1e-12
        sol, which = oracle(E, L, r3, dr0, r_end=r2, tau_max=1e6)
        if which != "turn" or not len(sol.t_events[1]): continue
        yv = sol.y_events[1][0]
        phi_o, t_o, tau_o = float(yv[2]), float(yv[3]), float(sol.t_events[1][0])
        r_fin = float(yv[0])   # the oracle's own (numeric) periapsis
        try:
            P = Param(E, L, "bound")
        except Exception:
            continue
        if not P.ok: continue
        # (a) Parametrization-free radial quadrature at the EXACT root
        #     endpoints r3 -> r2: r = r2 + (r3-r2) sin^2(th) absorbs the
        #     1/sqrt(R) singularity at BOTH turning points; no event, no
        #     endpoint bookkeeping. This is the control's accuracy number.
        dr_span = r3 - r2
        def rquad(npan):
            edges = np.linspace(0.0, 0.5*np.pi, npan+1)
            phi = t = tau = 0.0
            for i in range(npan):
                lo, hi = edges[i], edges[i+1]
                mid, half = 0.5*(lo+hi), 0.5*(hi-lo)
                th = mid + half*X4
                r = r2 + dr_span*np.sin(th)**2
                R = Rfun(r, E2, L2o)
                sq = np.sqrt(np.maximum(R, 0.0))
                dtau = 2.0*dr_span*np.sin(th)*np.cos(th)/sq
                dphi = (L/r**2)*dtau
                dt = (E/(1.0-2.0/r))*dtau
                phi += half*np.dot(W4, dphi); t += half*np.dot(W4, dt)
                tau += half*np.dot(W4, dtau)
            return phi, t, tau
        rq = {n: rquad(n) for n in (512, 2048, 4096)}
        rq_conv = max(abs(rq[2048][j]-rq[4096][j]) for j in range(3))
        # candidate: the turning points are eta = -pi (apoapsis) and eta = 0
        # (periapsis) BY CONSTRUCTION of the cos parametrization. Do NOT
        # invert u(eta) = 1/r there: arccos'(+-1) = inf, so a few-ulp error
        # in c = (u-f)/A becomes a ~1e-7 eta error (sqrt-amplified), and the
        # missing turning-point sliver costs a further ~sqrt(delta) in tau --
        # a flat, panel-independent offset of ~1e-9 relative. Same trap on
        # the cosh branch at eta = eta0 (arccosh'(1) = inf): plunge code must
        # use P.eta0 directly at turning points, as at_turn already does.
        ea, eb = -np.pi, 0.0
        rec = {"oracle_turn": [phi_o, t_o, tau_o], "r_peri_oracle": r_fin,
               "r2": float(r2), "r3": float(r3),
               "rquad_tau_4096": float(rq[4096][2]), "rquad_self_conv": float(rq_conv),
               "eta_span": float(abs(eb-ea)), "panels": {}}
        for npan in (8, 16, 32, 64):
            phi, t, tau = P.integrate(ea, eb, npan)
            rec["panels"][str(npan)] = [float(rel(phi-rq[4096][0], rq[4096][0])),
                                        float(rel(t-rq[4096][1], rq[4096][1])),
                                        float(rel(tau-rq[4096][2], rq[4096][2]))]
        # (b) The oracle leg, ended at its turn event: its numeric periapsis
        #     sits delta ~ 1e-12 below r2 and near periapsis dtau/dr ~
        #     1/sqrt(r-r2), so the comparison carries a flat bookkeeping
        #     floor ~ 2 sqrt(delta/R'(r2)) / tau_half, independent of panels.
        #     Recorded with its prediction, not hidden.
        rec["oracle_vs_rquad"] = [float(rel(phi_o-rq[4096][0], rq[4096][0])),
                                  float(rel(t_o-rq[4096][1], rq[4096][1])),
                                  float(rel(tau_o-rq[4096][2], rq[4096][2]))]
        Rp = -(2.0/r2**2 - 2.0*L2o/r2**3 + 6.0*L2o/r2**4)   # R'(r2) = -Veff'
        rec["floor_predicted"] = float(2.0*np.sqrt(abs(r_fin-r2)/Rp)/tau_o)
        bc[f"E2={E2:.6g}"] = rec
    res["bound_control_apo_to_peri"] = bc

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

    # ---- E7: near-separatrix valley: adaptive float bisection (kept, for
    #      comparison) AND the law's FIXED cut layout, oracle-verified ----
    res["separatrix_valley_panels_to_1e-11"] = separatrix_cost()
    lad = {}
    for d in (1e-2, 1e-4, 1e-6, 1e-8, 1e-10):
        E2 = Vmax*(1+d)
        real, _ = roots_R(E2, L2); r3 = real[real > 2][-1]
        o = valley_acc(np.sqrt(E2), np.sqrt(L2), "outer", r3, 3.0, at_turn=True)
        if o is not None: lad[f"d={d:g}"] = o
        if o is None: continue
        # (i) the B9-faithful rung ratio m=2 (2 panels per octave of
        #     distance-to-barrier-top), measured post-prediction: the
        #     pre-registered layout is m=1 above; m=2 diagnoses where the
        #     m=1 error lives (transition rungs) at +2J panels.
        try:
            P = Param(np.sqrt(E2), np.sqrt(L2), "outer")
            ea = P.eta0
            eb = P.eta_of_r(3.0, +1)
            e2, _ = ladder_edges(P, ea, eb, m=2)
            phi2, t2, tau2 = P.integrate_edges(e2, "factored")
        except Exception as ex:
            e2 = None
            o["ladder_m2_factored"] = {"fail": f"{type(ex).__name__}: {ex}"}
        if e2 is not None:
            phi_o, t_o, tau_o = o["oracle"]
            o["ladder_m2_factored"] = {"panels": int(len(e2)-1),
                "err": [float(rel(phi2-phi_o, phi_o)), float(rel(t2-t_o, t_o)),
                        float(rel(tau2-tau_o, tau_o))]}
        # (ii) the oracle's own error bar: rerun the truth at rtol 1e-13.
        #     Near the barrier top the stepper's error is amplified (the
        #     crossing time depends on E^2 like 1/delta), so at tiny delta the
        #     rtol-1e-12 truth is itself uncertain; record the shift.
        dr0 = -np.sqrt(max(Rfun(r3, E2, L2), 0.0)) or -1e-12
        sol13, which13 = oracle(np.sqrt(E2), np.sqrt(L2), r3, dr0, r_end=3.0,
                                tau_max=2e7, rtol=1e-13)
        if which13 == "plunge" and len(sol13.t_events[0]) and e2 is not None:
            yv = sol13.y_events[0][0]
            phi13, t13, tau13 = float(yv[2]), float(yv[3]), float(sol13.t_events[0][0])
            phi_o, t_o, tau_o = o["oracle"]
            o["oracle_shift_rtol13"] = [float(abs(phi13-phi_o)/phi_o),
                                        float(abs(t13-t_o)/t_o),
                                        float(abs(tau13-tau_o)/tau_o)]
            o["ladder_m2_factored"]["err_vs_rtol13"] = [
                float(rel(phi2-phi13, phi13)), float(rel(t2-t13, t13)),
                float(rel(tau2-tau13, tau13))]
    res["separatrix_valley_fixed_ladder"] = lad

    # ---- E8: kicks INTO the valley (the regime the plane actually refuses:
    #      a decaying orbit crosses Vmax arbitrarily closely) ----
    vk = {}
    E2b0 = 0.5*(Vmin+Vmax)
    realb, _ = roots_R(E2b0, L2); posb = np.sort(realb[realb > 2])
    r2b, r3b = posb[1], posb[2]
    for frac in (0.35, 0.7):
        r_k = r2b + frac*(r3b-r2b)
        sol, _ = oracle(np.sqrt(E2b0), np.sqrt(L2), r3b, -1e-12, r_end=r_k,
                        tau_max=1e6)
        if not len(sol.t_events[0]): continue
        phi_k = float(sol.y_events[0][0][2]); t_k = float(sol.y_events[0][0][3])
        tau_k = float(sol.t_events[0][0])
        for d in (1e-4, 1e-6, 1e-8):
            E2k = Vmax*(1+d); Ek = np.sqrt(E2k)
            dr_k = -np.sqrt(max(Rfun(r_k, E2k, L2), 0.0))
            sol2, which = oracle(Ek, np.sqrt(L2), r_k, dr_k, phi0=phi_k, t0=t_k,
                                 tau0=tau_k, r_end=3.0, tau_max=1e7)
            if which != "plunge": continue
            phi_o2 = float(sol2.y_events[0][0][2]); t_o2 = float(sol2.y_events[0][0][3])
            tau_o2 = float(sol2.t_events[0][0])
            rec = {"r_k": float(r_k), "E2k": float(E2k)}
            try:
                P = Param(Ek, np.sqrt(L2), "outer")
            except Exception:
                continue
            if P.ok:
                ea = P.eta_of_r(r_k, +1); eb = P.eta_of_r(3.0, +1)
                if ea is not None and eb is not None and eb > ea:
                    phi, t, tau = P.integrate(ea, eb, 64)
                    rec["uniform64"] = [float(rel(phi-(phi_o2-phi_k), phi_o2-phi_k)),
                                        float(rel(t-(t_o2-t_k), t_o2-t_k)),
                                        float(rel(tau-(tau_o2-tau_k), tau_o2-tau_k))]
                    edges, meta = ladder_edges(P, ea, eb)
                    rec["ladder"] = {}
                    for rform in ("fun", "factored"):
                        try:
                            phi, t, tau = P.integrate_edges(edges, rform)
                            rec["ladder"][rform] = {"panels": int(len(edges)-1),
                                "err": [float(rel(phi-(phi_o2-phi_k), phi_o2-phi_k)),
                                        float(rel(t-(t_o2-t_k), t_o2-t_k)),
                                        float(rel(tau-(tau_o2-tau_k), tau_o2-tau_k))]}
                        except ValueError as ex:
                            rec["ladder"][rform] = {"panels": int(len(edges)-1),
                                                    "fail": str(ex)}
                    m = dict(meta); m["panels"] = int(len(edges)-1)
                    rec["ladder_meta"] = m
                    try:
                        e2, _ = ladder_edges(P, ea, eb, m=2)
                        phi, t, tau = P.integrate_edges(e2, "factored")
                        rec["ladder_m2_factored"] = {"panels": int(len(e2)-1),
                            "err": [float(rel(phi-(phi_o2-phi_k), phi_o2-phi_k)),
                                    float(rel(t-(t_o2-t_k), t_o2-t_k)),
                                    float(rel(tau-(tau_o2-tau_k), tau_o2-tau_k))]}
                    except Exception as ex:
                        rec["ladder_m2_factored"] = {"fail": str(ex)}
            vk[f"frac={frac:g},d={d:g}"] = rec
    res["valley_kicks"] = vk

    res["wall_seconds"] = time.time()-t_start
    with open("metrics.json", "w") as f: json.dump(res, f, indent=1)
    print(json.dumps({k: v for k, v in res.items()
                      if k not in ("kick_across_separatrix",)}, indent=1))
    print("KICKS:", res["kick_across_separatrix"]["n"],
          res["kick_across_separatrix"]["err64_max_dphi_dt_dtau"])

# ---------------- E7 helper: adaptive float bisection (comparison only) ------------
def adaptive_panel_count(P, eta_a, eta_b, tol_int=1e-11, max_panels=20000):
    """Deterministic bisection refinement in eta; counts panels needed so each
    panel's GL4-vs-2xGL4 discrepancy is below tol_int. NOT the law's layout:
    float bisection that probes the integrand; kept to regenerate the
    historical adaptive counts next to the fixed-ladder ones."""
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
    L2s = 13.0
    ext = extrema(L2s); rU, rS = ext
    Vmaxs = Veff(rU, L2s)
    out = {}
    for d in (1e-2, 1e-4, 1e-6, 1e-8, 1e-10):
        E2 = Vmaxs*(1+d); E, L = np.sqrt(E2), np.sqrt(L2s)
        real, _ = roots_R(E2, L2s); r3 = real[real > 2][-1]
        P = Param(E, L, "outer")
        if not P.ok: out[f"d={d:g}"] = "param-fail"; continue
        eb = P.eta_of_r(3.0, +1)
        n = adaptive_panel_count(P, P.eta0, eb)
        out[f"d={d:g}"] = n
    return out

if __name__ == "__main__":
    main()
