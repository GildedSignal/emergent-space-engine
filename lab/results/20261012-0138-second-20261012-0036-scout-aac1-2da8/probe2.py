#!/usr/bin/env python3
"""Second-author probe (run 20261012-0138): the checker's named experiment for gold.

Churn census as a function of window (60 -> 600 radial periods, prefixes of ONE long
integration per orbit), with an angle-based libration classifier replacing the slope
t-stat, on a second potential (P2, centrally concentrated) and bar shape (A2, localized
oval), plus a bar-strength sweep for the doll-edge width. P1/A1 are the original run's
potential/bar, byte-identical physics. Circular orbits (de=0) get a closed-form compile
(the original's nfail=19 double-root edge).

Census JSONs regenerate from: python3 probe2.py <job>  (jobs listed in JOBS).
"""
import json, time, sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

# ---------- potentials ----------
def make_pot(V0, RC, GM, B):
    def phi(r):   return 0.5*V0*V0*np.log1p((r/RC)**2) - GM/np.sqrt(r*r + B*B)
    def dphi(r):  return V0*V0*r/(RC*RC + r*r) + GM*r/(r*r + B*B)**1.5
    def d2phi(r): return V0*V0*(RC*RC - r*r)/(RC*RC + r*r)**2 + GM*(2*r*r - B*B)/(r*r + B*B)**2.5
    def vc2(r):   return r*dphi(r)
    return dict(phi=phi, dphi=dphi, d2phi=d2phi, vc2=vc2)

POTS = dict(P1=make_pot(1.0, 0.5, 0.5, 0.2),    # the original run's potential
            P2=make_pot(1.0, 0.25, 0.8, 0.1))   # held out: centrally concentrated

# ---------- bars ----------
def A1(r):  return r*r/(r*r + 1.0)                       # original: extended
def dA1(r): return 2.0*r/(r*r + 1.0)**2
_S2 = 1.2*1.2
def A2(r):  q = (r*r)/_S2; return q*np.exp(1.0 - q)      # held out: localized oval, peak 1 at r=1.2
def dA2(r): q = (r*r)/_S2; return (2.0*r/_S2)*(1.0 - q)*np.exp(1.0 - q)
BARS = dict(A1=(A1, dA1), A2=(A2, dA2))

def rhs(t, s, potk, bark, eps, OmP):
    x, y, vx, vy = s
    r = np.sqrt(x*x + y*y)
    P = POTS[potk]; A, dA = BARS[bark]
    ar = -P['dphi'](r)
    th2 = 2.0*(np.arctan2(y, x) - OmP*t)
    c, sn = np.cos(th2), np.sin(th2)
    ar_p = -eps*dA(r)*c
    af_p = 2.0*eps*A(r)*sn/r
    return [vx, vy, (ar + ar_p)*x/r + af_p*(-y/r), (ar + ar_p)*y/r + af_p*(x/r)]

# ---------- cycle compilation from (E, L), with circular closed form ----------
GLN, GLP = 16, 12
_x, _w = np.polynomial.legendre.leggauss(GLN)
PSI  = np.pi*(np.arange(GLP)[:, None] + 0.5*_x[None, :] + 0.5)/GLP
WPSI = np.pi*_w[None, :]/(2*GLP)

def compile_cycle(potk, E, L):
    P = POTS[potk]
    def f(r): return L*L/(2*r*r) + P['phi'](r) - E
    rs = np.geomspace(1e-3, 300.0, 4000)
    fr = f(rs)
    i = np.where((fr[:-1]*fr[1:]) < 0)[0]
    if len(i) >= 2:
        rp = brentq(f, rs[i[0]],  rs[i[0]+1],  xtol=1e-13)
        ra = brentq(f, rs[i[-1]], rs[i[-1]+1], xtol=1e-13)
        if not (1e-3 < rp < ra < 299.0): raise ValueError("bad roots")
        c, Aa = 0.5*(ra+rp), 0.5*(ra-rp)
        r = c + Aa*np.cos(PSI)
        den = np.sqrt(np.maximum(2.0*(E - (L*L/(2*r*r) + P['phi'](r))), 1e-300))
        dt_dpsi = Aa*np.sin(PSI)/den
        dphi_dpsi = dt_dpsi*(L/(r*r))
        Tr = 2.0*np.sum(dt_dpsi*WPSI)
        dphi = 2.0*np.sum(dphi_dpsi*WPSI)
        return dict(circular=False, rp=rp, ra=ra, Tr=Tr, dphi=dphi,
                    OmR=2*np.pi/Tr, OmPhi=dphi/Tr)
    if len(i) == 0 and fr.min() < 1e-3:            # tangential double root: circular
        j = int(np.argmin(fr))
        xg = [rs[max(j-1, 0)], rs[j], rs[min(j+1, len(rs)-1)]]
        yg = [f(x) for x in xg]
        c0, c1, _ = np.polyfit(xg, yg, 2)
        rc = float(-c1/(2.0*c0))
        if not (1e-3 < rc < 299.0) or abs(f(rc)) > 1e-5: raise ValueError("no annulus")
        kap2 = P['d2phi'](rc) + 3.0*L*L/rc**4
        if kap2 <= 0: raise ValueError("bad circular")
        OmPhi = L/(rc*rc)
        return dict(circular=True, rp=rc, ra=rc, Tr=2*np.pi/np.sqrt(kap2),
                    dphi=2*np.pi*OmPhi/np.sqrt(kap2), OmR=np.sqrt(kap2), OmPhi=OmPhi)
    raise ValueError("no annulus")

# ---------- angle-based libration classifier (replaces slope t-stat) ----------
def classify_prefix(tp, phip, Lp, Ep, potk, OmP, OmR0):
    n = len(tp)
    Omphi_bar = (phip[-1]-phip[0])/(tp[-1]-tp[0])
    try:
        OmR_m = compile_cycle(potk, float(np.median(Ep)), float(np.median(Lp)))['OmR']
    except Exception:
        OmR_m = OmR0
    kstar = int(np.round(2.0*(Omphi_bar - OmP)/OmR_m))
    th = np.mod(2.0*phip - 2.0*OmP*tp - kstar*OmR_m*tp, 2*np.pi)
    Rbar = float(np.abs(np.mean(np.exp(1j*th))))
    n10 = max(1, n//10)
    L0m, L1m = float(np.median(Lp[:n10])), float(np.median(Lp[-n10:]))
    dL = abs(L1m-L0m)/abs(L0m)
    Ebar = abs(np.mean(Ep))
    dE = abs(float(np.median(Ep[-n10:])) - float(np.median(Ep[:n10])))/Ebar
    Ew = float((np.max(Ep)-np.min(Ep))/Ebar)
    A = np.vstack([tp, np.ones(n)]).T                      # original t-stat for comparison
    sl, ic = np.linalg.lstsq(A, Lp, rcond=None)[0]
    res = Lp - (sl*tp + ic)
    tstat = float(abs(sl)/(np.std(res)/np.sqrt(np.sum((tp-tp.mean())**2)) + 1e-300))
    cls = 'lib' if Rbar >= 0.5 else ('walk' if dL > 0.05 else 'quiet')
    return dict(cls=cls, Rbar=Rbar, dL=float(dL), dE=dE, Ew=Ew, kstar=kstar,
                OmR_m=float(OmR_m), tstat=tstat)

def resonance_radii(potk, OmP):
    P = POTS[potk]
    r = np.geomspace(0.05, 12.0, 20000)
    Om = np.sqrt(P['vc2'](r))/r
    kap = np.sqrt(np.maximum(P['d2phi'](r) + 3.0*P['dphi'](r)/r, 1e-12))
    out = {}
    for nm, g in (('corotation', Om - OmP), ('OLR', 2*(Om - OmP) + kap), ('ILR', 2*(Om - OmP) - kap)):
        s = np.where((g[:-1]*g[1:]) < 0)[0]
        out[nm] = [float(np.sqrt(r[i]*r[i+1])) for i in s]
    return out

# ---------- census ----------
BIN_EDGES = (0.0, 1.8, 2.3, 2.8, 4.2)

def census(tag, potk, bark, eps, OmP, seed, Tperiods, windows):
    P = POTS[potk]
    recs, nfail, t_cmp, t_int = [], 0, 0.0, 0.0
    t00 = time.perf_counter()
    rng = np.random.default_rng(seed)
    Rgs = np.linspace(0.35, 4.0, 19)
    epi = np.linspace(0.0, 0.3, 11)
    for Rg in Rgs:
        for de in epi:
            r0 = Rg*(1.0+de)
            vt = np.sqrt(P['vc2'](Rg))*Rg/r0
            E0 = 0.5*vt*vt + P['phi'](r0); L0 = r0*vt
            try:
                t0 = time.perf_counter(); cyc = compile_cycle(potk, E0, L0)
                t_cmp += time.perf_counter()-t0
            except Exception:
                nfail += 1; continue
            Tr = float(cyc['Tr']); T = Tperiods*Tr
            th0 = rng.uniform(0, 2*np.pi); c_, s_ = np.cos(th0), np.sin(th0)
            s0r = np.array([r0*c_, r0*s_, -vt*s_, vt*c_])
            te = np.linspace(0, T, int(4*Tperiods)+1)
            t0 = time.perf_counter()
            sol = solve_ivp(rhs, (0, T), s0r, args=(potk, bark, eps, OmP),
                            method='DOP853', rtol=1e-10, atol=1e-12, t_eval=te)
            t_int += time.perf_counter()-t0
            if not sol.success: nfail += 1; continue
            x, y = sol.y[0], sol.y[1]
            r = np.hypot(x, y); phi = np.unwrap(np.arctan2(y, x))
            L = x*sol.y[3] - y*sol.y[2]
            E = 0.5*(sol.y[2]**2 + sol.y[3]**2) + P['phi'](r)
            win = {}
            for W in windows:
                m = max(np.searchsorted(te, W*Tr, side='right'), 21)
                win[str(W)] = classify_prefix(te[:m], phi[:m], L[:m], E[:m], potk, OmP, cyc['OmR'])
            recs.append(dict(Rg=float(Rg), de=float(de), E0=float(E0), L0=float(L0), Tr=Tr,
                             OmR0=float(cyc['OmR']), OmPhi0=float(cyc['OmPhi']),
                             circular=bool(cyc['circular']), win=win))
        print(f"[{tag}] Rg={Rg:.2f} done, wall={time.perf_counter()-t00:.0f}s nfail={nfail}",
              flush=True)
    return dict(tag=tag, pot=potk, bar=bark, eps=eps, OmP=OmP, seed=seed,
                Tperiods=Tperiods, windows=list(windows), bin_edges=list(BIN_EDGES),
                n=len(recs), nfail=nfail, orbits=recs, t_int_s=t_int, t_cmp_s=t_cmp,
                resonances=resonance_radii(potk, OmP))

JOBS = {
    'p1-long':   dict(tag='p1-e03-600',  potk='P1', bark='A1', eps=0.03, OmP=0.5, seed=1717, Tperiods=600, windows=(60, 120, 240, 480, 600)),
    'p2-long':   dict(tag='p2-e03-600',  potk='P2', bark='A2', eps=0.03, OmP=0.5, seed=4242, Tperiods=600, windows=(60, 120, 240, 480, 600)),
    'p1e10-long':dict(tag='p1-e10-600',  potk='P1', bark='A1', eps=0.10, OmP=0.5, seed=4242, Tperiods=600, windows=(60, 120, 240, 480, 600)),
    'p1-s001':   dict(tag='p1-e001-60',  potk='P1', bark='A1', eps=0.01, OmP=0.5, seed=1717, Tperiods=60,  windows=(60,)),
    'p1-s03':    dict(tag='p1-e03-60',   potk='P1', bark='A1', eps=0.03, OmP=0.5, seed=4242, Tperiods=60,  windows=(60,)),
    'p1-s10':    dict(tag='p1-e10-60',   potk='P1', bark='A1', eps=0.10, OmP=0.5, seed=1717, Tperiods=60,  windows=(60,)),
    'p2-s001':   dict(tag='p2-e001-60',  potk='P2', bark='A2', eps=0.01, OmP=0.5, seed=4242, Tperiods=60,  windows=(60,)),
    'p2-s03':    dict(tag='p2-e03-60',   potk='P2', bark='A2', eps=0.03, OmP=0.5, seed=1717, Tperiods=60,  windows=(60,)),
    'p2-s10':    dict(tag='p2-e10-60',   potk='P2', bark='A2', eps=0.10, OmP=0.5, seed=4242, Tperiods=60,  windows=(60,)),
    'p1e001-long':dict(tag='p1-e001-600', potk='P1', bark='A1', eps=0.01, OmP=0.5, seed=1717, Tperiods=600, windows=(60, 120, 240, 480, 600)),
    'p2e10-long': dict(tag='p2-e10-600',  potk='P2', bark='A2', eps=0.10, OmP=0.5, seed=4242, Tperiods=600, windows=(60, 120, 240, 480, 600)),
}

if __name__ == '__main__':
    which = sys.argv[1]
    out = census(**JOBS[which])
    p = f"data/census-{out['tag']}.json"
    with open(p, 'w') as f: json.dump(out, f)
    print(f"wrote {p}: n={out['n']} nfail={out['nfail']} "
          f"t_int={out['t_int_s']:.0f}s t_cmp={out['t_cmp_s']:.2f}s", flush=True)
