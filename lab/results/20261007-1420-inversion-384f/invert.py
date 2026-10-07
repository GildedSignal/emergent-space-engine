#!/usr/bin/env python3
"""Inversion run 20261007-1420: attack the phase-neighbour certificate (gold 20261006-0346-taleb-09b5).

Truth: brute-force two-body Kepler propagation + KD-tree closest approach.
Certificates under test:
  A. phase-rank      : group bodies by orbit (quantized elements), sort by mean longitude
                       at window start, check k neighbours each side. (The gold's certificate.)
  B. window tier     : orbit-path-overlap candidates (geometric path distance < R_path).
                       (q-candidate-degree's tier that the gold says goes quadratic on formations.)
  C. time-rank@locus : rank bodies by ARRIVAL TIME at each orbit-crossing locus
                       (nodes, pericentre funnels); check k time-neighbours. (The inversion's repair.)
Units: mu=1, lengths in orbital radii (~1 AU). R_enc = 1e-3 (~150 km at 1 AU: ship-encounter scale).
"""
import numpy as np, json, sys, time
from scipy.spatial import cKDTree

R_ENC  = 1e-3   # encounter radius
R_PATH = 2e-3   # orbit-path overlap threshold for window-tier candidacy
K      = 4      # the gold's rank
R_LOCUS= 5e-3   # locus detection radius

# ---------------- Kepler ----------------
def kepler_E(M, e):
    E = M.copy()
    for _ in range(60):
        f  = E - e*np.sin(E) - M
        fp = 1 - e*np.cos(E)
        d  = f/fp
        E  = E - d
        if np.max(np.abs(d)) < 1e-14: break
    return E

def positions(a, e, om, M0, n, t):
    M = M0 + n*t
    E = kepler_E(M % (2*np.pi), e)
    x = a*(np.cos(E) - e)
    y = a*np.sqrt(1-e**2)*np.sin(E)
    c, s = np.cos(om), np.sin(om)
    return np.stack([x*c - y*s, x*s + y*c], axis=1)

def orbit_samples(a, e, om, N=2000):
    E = np.linspace(0, 2*np.pi, N)
    x = a*(np.cos(E) - e); y = a*np.sqrt(1-e**2)*np.sin(E)
    c, s = np.cos(om), np.sin(om)
    return np.stack([x*c - y*s, x*s + y*c], axis=1)

# ---------------- truth ----------------
def truth(bodies, window, dt_coarse, v_max):
    """brute force: coarse KD pass, then per-flagged-pair refinement."""
    a,e,om,M0,n = bodies
    R_c = R_ENC + v_max*dt_coarse          # cannot hop over
    pairs_min = {}
    t = 0.0
    while t < window:
        P = positions(a,e,om,M0,n,t)
        tr = cKDTree(P)
        for (i,j) in tr.query_pairs(R_c):
            d = np.linalg.norm(P[i]-P[j])
            key = (i,j)
            if key not in pairs_min or d < pairs_min[key][0]:
                pairs_min[key] = (d, t)
        t += dt_coarse
    enc = set()
    for (i,j),(d0,t0) in pairs_min.items():
        # refine on fine grid around t0 (and around window edges if never coarse-hit near)
        ts = t0 + np.arange(-8, 9)*dt_coarse/16
        ts = ts[(ts>=0)&(ts<window)]
        best = 1e9
        for tt in ts:
            P = positions(a[i:i+1],e[i],om[i],M0[i:i+1],n[i],tt)
            Q = positions(a[j:j+1],e[j],om[j],M0[j],n[j],tt)
            best = min(best, np.linalg.norm(P[0]-Q[0]))
        if best < R_ENC: enc.add((i,j))
    return enc

# ---------------- certificates ----------------
def group_orbits(a, e, om, tol_a=1e-3, tol_e=5e-3, tol_om=2e-2):
    N = len(a); gid = np.full(N, -1); g = 0
    for i in range(N):
        if gid[i] >= 0: continue
        gid[(np.abs(a-a[i])/a[i]<tol_a)&(np.abs(e-e[i])<tol_e)&(np.abs(((om-om[i]+np.pi)%(2*np.pi))-np.pi)<tol_om)] = g
        g += 1
    return gid

def phase_rank(bodies, gid, k=K, window=0.0, both_ends=True):
    a,e,om,M0,n = bodies
    checked = set()
    for g in np.unique(gid):
        idx = np.where(gid==g)[0]
        lam = (om[idx] + M0[idx]) % (2*np.pi)          # mean longitude at window start
        order = idx[np.argsort(lam)]
        for r in range(len(order)):
            for dr in range(1, k+1):
                for rr in (r-dr, r+dr):
                    if 0 <= rr < len(order):
                        i,j = sorted((order[r], order[rr])); checked.add((i,j))
        if both_ends:                                    # also ordering at window end
            lam2 = (lam + n[idx]*window) % (2*np.pi)
            order = idx[np.argsort(lam2 % (2*np.pi))]
            for r in range(len(order)):
                for dr in range(1, k+1):
                    for rr in (r-dr, r+dr):
                        if 0 <= rr < len(order):
                            i,j = sorted((order[r], order[rr])); checked.add((i,j))
    return checked

def window_tier(bodies, gid):
    """candidate pairs = every pair whose ORBIT PATHS approach within R_PATH."""
    a,e,om,M0,n = bodies
    gs = np.unique(gid); samples = {g: orbit_samples(a[gid==g][0], e[gid==g][0], om[gid==g][0], N=300) for g in gs}
    SPACING_T = 2*np.pi*np.max(a)/300                    # coarse-grid tolerance
    counts = {g: int((gid==g).sum()) for g in gs}
    cand = 0; gl = list(gs)
    trees = {g: cKDTree(samples[g]) for g in gl}
    for ii in range(len(gl)):
        for jj in range(ii, len(gl)):
            gi, gj = gl[ii], gl[jj]
            d, _ = trees[gi].query(samples[gj], k=1)
            if d.min() < R_PATH + SPACING_T:
                cand += counts[gi]*counts[gj] if gi!=gj else counts[gi]*(counts[gi]-1)//2
    return cand

def time_rank_locus(bodies, gid, window, k=K, fine=False):
    """rank bodies by ARRIVAL TIME at each spatial locus where orbit families cross.
    (Same-family encounters are phase rank's job; here only inter-family loci.)"""
    a,e,om,M0,n = bodies
    gs = np.unique(gid); trees = {}; samples = {}
    NS = 2000 if fine else 300
    Eg = np.linspace(0, 2*np.pi, NS)                      # grid for detection
    for g in gs:
        samples[g] = orbit_samples(a[gid==g][0], e[gid==g][0], om[gid==g][0], N=NS)
        trees[g]   = cKDTree(samples[g])
    # locus points: where two DIFFERENT families' paths pass within detection radius
    SPACING = 2*np.pi*np.max(a)/NS                        # grid resolution
    R_DET = R_LOCUS + SPACING                            # sampling-tolerant detection
    pts = []
    gl = list(gs)
    for ii in range(len(gl)):
        for jj in range(ii+1, len(gl)):
            d, _ = trees[gl[ii]].query(samples[gl[jj]], k=1)
            if d.min() < R_DET: pts.append(samples[gl[jj]][d < R_DET])
    if not pts: return set()
    pts = np.vstack(pts)
    if len(pts) > 20000:                                   # loci detection needs a sample, not all
        pts = pts[np.random.default_rng(0).choice(len(pts), 20000, replace=False)]
    lt = cKDTree(pts); used = np.zeros(len(pts), bool); loci = []
    for h in range(len(pts)):
        if used[h]: continue
        grp = lt.query_ball_point(pts[h], R_DET); used[grp] = True
        loci.append(pts[grp].mean(axis=0))
    # refine each locus to the exact consensus point of the family curves
    # (the gate must sit ~1e-4 from the true intersection or the arrival
    #  ordering smears by delta/v; alternating projection converges there)
    def curve_pt(g, L):
        a_g, e_g, om_g = a[gid==g][0], e[gid==g][0], om[gid==g][0]
        dd = np.linalg.norm(samples[g]-L, axis=1); i0 = int(np.argmin(dd))
        loE, hiE = Eg[i0]-2*np.pi/150, Eg[i0]+2*np.pi/150
        c, s = np.cos(om_g), np.sin(om_g)
        def pv(E):
            x = a_g*(np.cos(E)-e_g); y = a_g*np.sqrt(1-e_g**2)*np.sin(E)
            return np.array([x*c-y*s, x*s+y*c])
        for _ in range(24):
            m1 = loE+(hiE-loE)/3; m2 = hiE-(hiE-loE)/3
            if np.linalg.norm(pv(m1)-L) < np.linalg.norm(pv(m2)-L): hiE = m2
            else: loE = m1
        return pv(0.5*(loE+hiE))
    loci_r = []
    for L in loci:
        fams = [g for g in gl if np.min(np.linalg.norm(samples[g]-L, axis=1)) <= R_DET]
        for _ in range(2 if len(fams) > 12 else 40):
            Ln = np.mean([curve_pt(g, L) for g in fams], axis=0)
            if np.linalg.norm(Ln-L) < 1e-10: L = Ln; break
            L = Ln
        loci_r.append(L)
    loci = loci_r
    checked = set()
    for L in loci:
        arrivals = []
        for g in gl:
            idx = np.where(gid==g)[0]
            a_g, e_g, om_g = a[idx[0]], e[idx[0]], om[idx[0]]
            dd = np.linalg.norm(samples[g] - L, axis=1)
            i0 = int(np.argmin(dd))
            if dd[i0] > R_DET: continue                  # family passes near L
            # refine the family's crossing anomaly by local dense sampling
            dE = 2*np.pi/300*1.5
            Ef = np.linspace(Eg[i0]-dE, Eg[i0]+dE, 512)
            xs = a_g*(np.cos(Ef) - e_g); ys = a_g*np.sqrt(1-e_g**2)*np.sin(Ef)
            c, s = np.cos(om_g), np.sin(om_g)
            finepos = np.stack([xs*c - ys*s, xs*s + ys*c], axis=1)
            for Estar in Ef[np.argsort(np.linalg.norm(finepos - L, axis=1))[:2]]:
                Mf = Estar - e_g*np.sin(Estar)           # family crossing mean anomaly (seed)
                P = 2*np.pi/n[idx]
                tt = ((Mf - M0[idx])/n[idx]) % P
                for qq in range(int(window//P.max())+2):
                    t = tt + qq*P
                    if fine:
                        m = (t > 0) & (t < window)
                        arrivals.extend(zip(idx[m], t[m]))
                        continue
                    for i, tc in zip(idx, t):
                        if not (0 < tc < window): continue
                        # per-body arrival = closest approach to the SAME locus point L
                        # (shared geometric rule => family-systematic offsets cancel in rank)
                        lo, hi = tc-0.3, tc+0.3
                        for _ in range(34):
                            m1 = lo + (hi-lo)/3; m2 = hi - (hi-lo)/3
                            p1 = positions(a[i:i+1],e[i:i+1],om[i:i+1],M0[i:i+1],n[i:i+1],m1)[0]
                            p2 = positions(a[i:i+1],e[i:i+1],om[i:i+1],M0[i:i+1],n[i:i+1],m2)[0]
                            if np.linalg.norm(p1-L) < np.linalg.norm(p2-L): hi = m2
                            else: lo = m1
                        arrivals.append((i, 0.5*(lo+hi)))
        arrivals.sort(key=lambda z: z[1])
        for r in range(len(arrivals)):
            for dr in range(1, k+1):
                for rr in (r-dr, r+dr):
                    if 0 <= rr < len(arrivals):
                        i,j = sorted((arrivals[r][0], arrivals[rr][0])); checked.add((i,j))
    return checked

# ---------------- scenes ----------------
def scene_formation(n=240, seed=7, arc=0.15, sig_a=0.0):
    r = np.random.default_rng(seed)
    a = 1 + sig_a*r.standard_normal(n)
    e = np.zeros(n); om = np.zeros(n)
    M0 = r.uniform(-arc/2, arc/2, n)
    return (a,e,om,M0, np.power(a,-1.5))

def scene_crossing(nA=200, nB=200, seed=11, arcA=0.15, arcB=0.25, aB=2.0, eB=0.51):
    # ring formation a=1 + elliptical formation a=2,e=.51 (q=.98,Q=3.02) -> orbits cross at 2 nodes (+-0.345 rad)
    # both clumps timed to funnel through the +node near t=0.2
    r = np.random.default_rng(seed)
    aA = np.ones(nA); eA = np.zeros(nA); omA = np.zeros(nA)
    M0A = r.uniform(0.145-arcA/2, 0.145+arcA/2, nA)       # ring clump reaches node (0.345 rad) at t~0.2
    aBv = np.full(nB, aB); eBv = np.full(nB, eB); omBv = np.zeros(nB)
    M0B = r.uniform(0.027-arcB/2, 0.027+arcB/2, nB)       # ellipse clump reaches node at t~0.2
    a = np.concatenate([aA,aBv]); e = np.concatenate([eA,eBv]); om = np.concatenate([omA,omBv])
    M0 = np.concatenate([M0A,M0B]); n = np.power(a,-1.5)
    return (a,e,om,M0,n), nA

def scene_funnel(n=160, seed=13, spread=0.7, window=6.0, tspan=0.3):
    # distinct orbits sharing the SAME pericentre point (omega=0, q=0.98); passages clustered in time
    r = np.random.default_rng(seed)
    q = 0.98
    a = r.uniform(1.2, 1.2+spread, n)
    e = 1 - q/a; om = np.zeros(n)
    P = 2*np.pi*np.power(a,1.5)
    t_peri = r.uniform(0, tspan, n)
    M0 = (-t_peri/P % 1.0)*2*np.pi                        # pericentre passage at t_peri
    return (a,e,om,M0,np.power(a,-1.5))

def density_contrast(bodies, t=0.0, R=0.05):
    a,e,om,M0,n = bodies
    P = positions(a,e,om,M0,n,t)
    tr = cKDTree(P)
    cnt = np.array([len(x) for x in tr.query_ball_point(P, R)], float)
    mean = len(P)/(np.pi*(np.max(np.linalg.norm(P,axis=1))+R)**2)
    return cnt.max()/max(mean,1e-12)

def report(name, bodies, window, dt, vmax, split=None, run_time_locus=True, fine=False):
    a,e,om,M0,n = bodies
    gid = group_orbits(a,e,om)
    t0=time.time()
    E = truth(bodies, window, dt, vmax)
    tE = time.time()-t0
    groups = {int(g): int((gid==g).sum()) for g in np.unique(gid)}
    pr8 = phase_rank(bodies, gid, k=8, window=window)
    pr = phase_rank(bodies, gid, window=window)
    wt = window_tier(bodies, gid)
    tr_ = time_rank_locus(bodies, gid, window, fine=fine) if run_time_locus else set()
    tr8 = time_rank_locus(bodies, gid, window, k=8, fine=fine) if run_time_locus else set()
    def miss(checked):
        return len(E - checked)
    crossE = [p for p in E if split and gid[p[0]]!=gid[p[1]]]
    # two INDEPENDENT concentration axes:
    #  standing phase concentration (formation): peak mean-longitude histogram within largest group
    #  flux concentration (lanes/funnels): peak arrival-time histogram at loci
    lam = (om + M0) % (2*np.pi)
    big = np.bincount(gid).argmax(); lg = lam[gid==big]
    h,_ = np.histogram(lg, bins=np.arange(0, 2*np.pi+0.05, 0.05))
    phase_conc = round(float(h.max()) / max(len(lg)*0.05/(2*np.pi), 1e-9), 1)  # vs uniform
    crossS = set(crossE); interS = E - crossS
    def rec(cs, s):  # recall of checked-set cs over set s
        return round(1 - len(s - cs)/max(len(s),1), 4)
    uni = pr | tr_
    out = dict(scene=name, N=len(a), window=window, groups=groups,
               truth_encounters=len(E), truth_cross=len(crossE), truth_internal=len(interS),
               truth_time=round(tE,1),
               phase_rank=dict(checks=len(pr),
                               recall_cross=rec(pr, crossS), recall_internal=rec(pr, interS),
                               recall=rec(pr, E), recall_k8=rec(pr8, E)),
               window_tier=dict(candidates=wt, cand_per_enc=round(wt/max(len(E),1),1)),
               time_rank_locus=dict(checks=len(tr_),
                               recall_cross=rec(tr_, crossS), recall_internal=rec(tr_, interS),
                               recall=rec(tr_, E), recall_k8=rec(tr8, E)),
               union_recall=rec(uni, E), union_checks=len(uni),
               phase_conc_vs_uniform=phase_conc,
               max_group_frac=round(max(groups.values())/len(a),3))
    return out, E, gid

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv)>1 else "all"
    res = {}
    if which in ("s1","all"):
        b = scene_formation()
        res["S1_formation"],_,_ = report("S1 formation (gold's regime)", b, window=6.5, dt=2.5e-3, vmax=1.05)
    if which in ("s2","all"):
        b, nA = scene_crossing()
        res["S2_crossing"],_,_ = report("S2 crossing lanes (ring + ellipse formations)", b, window=9.0, dt=2.0e-3, vmax=1.7, split=True)
    if which in ("s2scale","all"):
        for npg in (100, 200, 400):
            # fixed linear density: arcs grow with n so real encounters ~ n, exposing any n^2 tier
            b, nA = scene_crossing(nA=npg, nB=npg, seed=11+npg,
                                   arcA=0.15*npg/200, arcB=0.25*npg/200)
            r,E,gid = report(f"S2 n={npg}/group (fixed density)", b, window=9.0, dt=2.5e-3, vmax=1.7,
                             split=True, run_time_locus=False)
            res[f"S2_n{npg}"] = r
    if which == "s2fine":
        b, nA = scene_crossing()
        res["S2_fine_gate"],_,_ = report("S2 crossing, fine gate (NS=2000 mutual-proximity locus, family-seeded arrivals)",
                                         b, window=9.0, dt=2.0e-3, vmax=1.7, split=True, fine=True)
    if which in ("s3","all"):
        b = scene_funnel(window=6.0)
        res["S3_funnel"],_,_ = report("S3 pericentre funnel (all singleton orbits)", b, window=6.0, dt=2.5e-3, vmax=1.6, split=True)
    print(json.dumps(res, indent=1))
