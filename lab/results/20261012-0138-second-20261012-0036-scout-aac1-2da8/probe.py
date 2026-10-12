#!/usr/bin/env python3
"""Galaxy doll falsifier: (E,L) cycle compilation vs stepping, regime chosen by compiled frequencies.

2D galaxy: log-core halo + Miyamoto-Nagai slice (analytic Phi, dPhi).
Truth: DOP853 rtol 1e-10 in Phi + m=2 rotating bar perturbation.
Candidate: cycle compiled from (E0, L0) by 1D radial quadrature (roots + psi panels);
           frequencies (OmR, OmPhi) feed the resonance detector m(OmPhi-OmP) ~ k OmR.
"""
import json, time, sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

# ---- potential (analytic, galaxy-like: rising then flat rotation curve) ----
V0, RC, GM, B = 1.0, 0.5, 0.5, 0.2
def phi_grav(r):  return 0.5*V0*V0*np.log1p((r/RC)**2) - GM/np.sqrt(r*r + B*B)
def dphi_dr(r):   return V0*V0*r/(RC*RC + r*r) + GM*r/(r*r + B*B)**1.5
def v_circ(r):    return np.sqrt(r*dphi_dr(r))

# ---- bar perturbation eps * A(r) cos(2(phi - OmP t)) ----
RB = 1.0
def A_bar(r):     return V0*V0*r*r/(r*r + RB*RB)
def dA_bar(r):    return V0*V0*2*r*RB*RB/(r*r + RB*RB)**2

def rhs(t, s, eps, OmP):
    x, y, vx, vy = s
    r = np.sqrt(x*x + y*y)
    ar = -dphi_dr(r)
    th2 = 2.0*(np.arctan2(y, x) - OmP*t)
    c, sn = np.cos(th2), np.sin(th2)
    ar_p = -eps*dA_bar(r)*c            # radial part of -grad(dPhi)
    af_p = 2.0*eps*A_bar(r)*sn/r       # azimuthal part
    ax = (ar + ar_p)*x/r + af_p*(-y/r)
    ay = (ar + ar_p)*y/r + af_p*(x/r)
    return [vx, vy, ax, ay]

def energy(s):    x, y, vx, vy = s; return 0.5*(vx*vx+vy*vy) + phi_grav(np.hypot(x, y))
def angmom(s):    x, y, vx, vy = s; return x*vy - y*vx

# ---- cycle compilation from (E, L): roots, T_r, dphi via psi panels ----
GLN, GLP = 16, 12                      # nodes per panel, panels
_x, _w = np.polynomial.legendre.leggauss(GLN)
PSI = np.pi*(np.arange(GLP)[:, None] + 0.5*_x[None, :] + 0.5)/GLP   # (GLP, GLN), panel-major
WPSI = np.pi*_w[None, :]/(2*GLP)

def compile_cycle(E, L):
    def f(r): return L*L/(2*r*r) + phi_grav(r) - E
    rs = np.geomspace(1e-3, 300.0, 4000)
    fr = f(rs)
    i = np.where((fr[:-1]*fr[1:]) < 0)[0]
    if len(i) < 2: raise ValueError("no annulus")
    rp = brentq(f, rs[i[0]], rs[i[0]+1], xtol=1e-13)
    ra = brentq(f, rs[i[-1]], rs[i[-1]+1], xtol=1e-13)
    if not (1e-3 < rp < ra < 299.0): raise ValueError("bad roots")
    c, A = 0.5*(ra+rp), 0.5*(ra-rp)
    r = c + A*np.cos(PSI)
    den = np.sqrt(np.maximum(2.0*(E - (L*L/(2*r*r) + phi_grav(r))), 1e-300))
    dt_dpsi = A*np.sin(PSI)/den
    dphi_dpsi = dt_dpsi*(L/(r*r))
    Tr = 2.0*np.sum(dt_dpsi*WPSI)
    dphi = 2.0*np.sum(dphi_dpsi*WPSI)
    t_tab = np.concatenate(([0.0], np.cumsum((dt_dpsi*WPSI).ravel())))
    ph_tab = np.concatenate(([0.0], np.cumsum((dphi_dpsi*WPSI).ravel())))
    return dict(rp=rp, ra=ra, Tr=Tr, dphi=dphi, OmR=2*np.pi/Tr, OmPhi=dphi/Tr,
                t_tab=t_tab, ph_tab=ph_tab, r_tab=r.ravel())

def eval_pos(cyc, t):
    """position (r, phi) at time t from compiled tables; inbound half mirrors the outbound."""
    Tr, Th = cyc['Tr'], 0.5*cyc['Tr']
    tm = np.mod(t, Tr)
    tm2 = np.where(tm > Th, Tr - tm, tm)     # mirrored leg time
    i = np.clip(np.searchsorted(cyc['t_tab'], tm2), 1, len(cyc['r_tab'])-1)
    f = (tm2 - cyc['t_tab'][i-1])/(cyc['t_tab'][i] - cyc['t_tab'][i-1])
    r = cyc['r_tab'][i-1] + f*(cyc['r_tab'][i] - cyc['r_tab'][i-1])
    ph_leg = cyc['ph_tab'][i-1] + f*(cyc['ph_tab'][i] - cyc['ph_tab'][i-1])
    ph_max = cyc['ph_tab'][-1]
    phi = np.where(tm <= Th, ph_leg, ph_max + (ph_max - ph_leg))
    return r, phi

def classify(Lt, Et, t):
    """walk vs bounded by slope t-stat on L(t); also E wobble."""
    n = len(t)
    A = np.vstack([t, np.ones(n)]).T
    sl, ic = np.linalg.lstsq(A, Lt, rcond=None)[0]
    res = Lt - (sl*t + ic)
    tstat = abs(sl)/(np.std(res)/np.sqrt(np.sum((t-t.mean())**2)) + 1e-300)
    dL = abs(np.median(Lt[-n//10:]) - np.median(Lt[:n//10]))/abs(np.median(Lt[:n//10]))
    Ew = (np.max(Et)-np.min(Et))/abs(np.mean(Et))
    return tstat, dL, Ew

def run_population(tag, n, eps, OmP, seed, t_end_periods=60.0):
    rng = np.random.default_rng(seed)
    Rgs = np.linspace(0.35, 4.0, int(np.sqrt(n)))
    n_epi = int(np.ceil(n/len(Rgs)))
    epi = np.linspace(0.0, 0.3, n_epi)
    recs, t_int, t_cmp = [], 0.0, 0.0
    nfail = 0
    for Rg in Rgs:
        for de in epi:
            r0 = Rg*(1.0+de)
            vt = v_circ(Rg)*Rg/r0            # L of circular at Rg
            s0 = np.array([r0, 0.0, 0.0, vt])
            E0, L0 = energy(s0), angmom(s0)
            try:
                t0 = time.perf_counter(); cyc = compile_cycle(E0, L0); t_cmp += time.perf_counter()-t0
            except Exception:
                nfail += 1; continue
            T = t_end_periods*cyc['Tr']
            th0 = rng.uniform(0, 2*np.pi)
            c_, s_ = np.cos(th0), np.sin(th0)
            s0r = np.array([r0*c_, r0*s_, -vt*s_, vt*c_])
            te = np.linspace(0, T, 240)
            t0 = time.perf_counter()
            sol = solve_ivp(rhs, (0, T), s0r, args=(eps, OmP), method='DOP853',
                            rtol=1e-10, atol=1e-12, t_eval=te)
            t_int += time.perf_counter()-t0
            if not sol.success: nfail += 1; continue
            Et = 0.5*(sol.y[2]**2+sol.y[3]**2) + phi_grav(np.hypot(sol.y[0], sol.y[1]))
            Lt = sol.y[0]*sol.y[3] - sol.y[1]*sol.y[2]
            tstat, dL, Ew = classify(Lt, Et, te)
            recs.append(dict(Rg=float(Rg), de=float(de), OmR=cyc['OmR'], OmPhi=cyc['OmPhi'],
                             Tr=cyc['Tr'], dphi=cyc['dphi'], tstat=float(tstat), dL=float(dL),
                             Ew=float(Ew), walk=bool(tstat > 4.0)))
    ws = np.linspace(0.02, 0.30, 15)
    sweep = []
    for w in ws:
        d = np.array([min(abs(2*(r['OmPhi']-OmP)/r['OmR'] - k) for k in (-2, -1, 0, 1, 2)) for r in recs])
        flag = d < w
        walk = np.array([r['walk'] for r in recs])
        tp, fp = int((flag & walk).sum()), int((flag & ~walk).sum())
        sweep.append(dict(w=float(w), recall=tp/max(walk.sum(), 1), fpr=fp/max((~walk).sum(), 1),
                          flagged=float(flag.mean())))
    ok = [s for s in sweep if s['fpr'] <= 0.20]
    best = max(ok, key=lambda s: s['recall']) if ok else None
    return dict(tag=tag, n=len(recs), nfail=nfail, eps=eps, OmP=OmP,
                walk_frac=float(np.mean([r['walk'] for r in recs])),
                best_w=best, sweep=sweep, orbits=recs,
                t_int_s=t_int, t_cmp_s=t_cmp)

def main():
    out = {}
    t0 = time.perf_counter()
    out['main'] = run_population('main eps=0.03', 384, 0.03, 0.5, 1717)
    # position-eval cost + accuracy vs truth on one compiled epicyclic orbit (eps=0: pure Phi)
    s0 = np.array([1.3, 0, 0, v_circ(1.2)*1.2/1.3])
    cyc = compile_cycle(energy(s0), angmom(s0))
    ts = np.random.default_rng(0).uniform(0, 40*cyc['Tr'], 20000)
    ts.sort()
    t1 = time.perf_counter(); [eval_pos(cyc, t) for t in ts[:2000]]; t_eval = (time.perf_counter()-t1)/2000
    sol = solve_ivp(rhs, (0, ts.max()), s0, args=(0.0, 0.5), method='DOP853',
                    rtol=1e-12, atol=1e-13, t_eval=ts)
    rr = np.hypot(sol.y[0], sol.y[1])
    r_c, _ = eval_pos(cyc, ts)
    out['eval'] = dict(compile_us=1e6*out['main']['t_cmp_s']/out['main']['n'],
                       step_us_per_orbit=1e6*out['main']['t_int_s']/out['main']['n'],
                       eval_us=1e6*t_eval, Tr=float(cyc['Tr']),
                       max_rel_r_err_over40Tr=float(np.nanmax(np.abs(r_c-rr)/rr)),
                       median_rel_r_err=float(np.nanmedian(np.abs(r_c-rr)/rr)))
    out['H1_eps10'] = run_population('H1 eps=0.10', 192, 0.10, 0.5, 4242)
    out['H2_OmP'] = run_population('H2 OmP=0.625', 192, 0.03, 0.625, 4242)
    out['wall_s'] = time.perf_counter()-t0
    with open(sys.argv[1] if len(sys.argv) > 1 else 'data/probe.json', 'w') as f:
        json.dump(out, f)
    for tag in ('main', 'H1_eps10', 'H2_OmP'):
        r = out[tag]
        print(f"[{r['tag']}] n={r['n']} fail={r['nfail']} walk_frac={r['walk_frac']:.3f} "
              f"best_w={r['best_w']}")
        print('   sweep:', [(round(s['w'], 2), round(s['recall'], 2), round(s['fpr'], 2)) for s in r['sweep'][::3]])
    print('eval:', out['eval'])
    print('wall_s:', round(out['wall_s'], 1))

if __name__ == '__main__':
    main()
