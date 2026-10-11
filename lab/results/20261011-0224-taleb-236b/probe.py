#!/usr/bin/env python3
"""Probe: does a phase-neighbour (rank-k) encounter certificate survive
co-orbital families whose dispersion is not shear?

Truth: exact two-body Kepler motion about one parent (GM=1, a0=1).
Contact: pair min distance < R over the horizon.
Rank: |index difference| in the fleet's mean-anomaly ordering at contact time
      (a conjunction passes through rank 0; a crossing never does).
Scenarios:
  S0 shear   : one-orbit formation, pure a-dispersion (the certificate's home ground)
  S1 family  : collision family, same a, e-vector dispersed (crossing-dominated)
  S2 intercpt: two phase-clumped fleets on crossing ellipses (interception)
  S4 mixed   : realistic tight formation with small e-vector spread (both branches)
Outputs metrics.json + prints a summary. Deterministic (seed fixed).
"""
import json, sys, time
import numpy as np
from scipy.spatial import cKDTree

GM = 1.0
A0 = 1.0
R = float(sys.argv[1]) if len(sys.argv) > 1 else 1e-4   # contact radius
K = 4                                                    # certificate partner rank
SEED = 20261011

def kepler_xy(a, e, w, M):
    E = M.copy()
    for _ in range(14):
        E = E - (E - e*np.sin(E) - M) / (1.0 - e*np.cos(E))
    r = a * (1.0 - e*np.cos(E))
    th = 2.0*np.arctan2(np.sqrt(1.0+e)*np.sin(E/2), np.sqrt(1.0-e)*np.cos(E/2))
    return np.stack([r*np.cos(th+w), r*np.sin(th+w)], axis=-1)

def M_of_theta(theta, e):
    E = 2.0*np.arctan2(np.sqrt(1.0-e)*np.sin(theta/2), np.sqrt(1.0+e)*np.cos(theta/2))
    return E - e*np.sin(E)

rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------- families
# each returns dict(a,e,w,M0, periods, steps_per_period, r_coarse, frozen)
def shear_control(n=500):
    # one-ellipse stream: neighbour spacing ~2.5*sigma/n = 1.5e-3 >> R (no birth
    # adjacency); drift reach 1.5*sqrt(2)*3e-4*6*2pi = 0.024 rad >> spacing => real catch-ups
    a = A0*(1.0 + rng.normal(0, 3e-4, n)); a.sort()
    return dict(a=a, e=np.full(n, 0.01), w=np.zeros(n),
                M0=rng.normal(0.0, 0.03, n), periods=6, spP=32,
                r_coarse=R + 2e-4, frozen=False)

def collision_family(n=1600):
    e = np.clip(0.1*(1.0 + rng.normal(0, 0.03, n)), 0.02, None)
    return dict(a=np.full(n, A0), e=e, w=rng.uniform(0, 2*np.pi, n),
                M0=rng.uniform(0, 2*np.pi, n), periods=1, spP=2048,
                r_coarse=R + 1.5e-3, frozen=True)

def interception(n_each=400):
    dw = np.deg2rad(120.0); eB = 0.05
    dM = (M_of_theta(dw/2 - dw, eB) - M_of_theta(dw/2, eB)) % (2*np.pi)
    n = 2*n_each
    return dict(a=np.full(n, A0), e=np.full(n, eB),
                w=np.concatenate([np.zeros(n_each), np.full(n_each, dw)]),
                M0=np.concatenate([rng.normal(0.0, np.deg2rad(3.0), n_each),
                                   rng.normal(0.0, np.deg2rad(3.0), n_each) + dM]),
                periods=1, spP=2048, r_coarse=R + 8e-3, frozen=True)

def mixed_formation(n=300):
    # tight formation (3.4 deg): sigma_a=2e-4, sigma_e=2e-3, omega spread 0.1 rad;
    # conjunction branch (rank~0) and crossing branch (rank ~ n*|dM*|/2pi) coexist
    a = A0*(1.0 + rng.normal(0, 2e-4, n)); a.sort()
    e = np.clip(0.01 + rng.normal(0, 2e-3, n), 1e-4, None)
    return dict(a=a, e=e, w=rng.normal(0.0, 0.1, n), M0=rng.normal(0.0, 0.06, n),
                periods=24, spP=16, r_coarse=R + 6e-3, frozen=False)

# ---------------------------------------------------------------- truth
def find_contacts(fam):
    a, e, w, M0 = fam['a'], fam['e'], fam['w'], fam['M0']
    n = len(a); nv = np.sqrt(GM/a**3)                    # per-ship mean motion
    n0 = nv.mean()
    T = fam['periods']*fam['spP']
    dt = (2*np.pi/n0)/fam['spP']
    F, D, TI = [], [], []                                 # flat pair idx, dist, step
    for it in range(T):
        xy = kepler_xy(a, e, w, M0 + nv*(it+0.5)*dt)
        pairs = cKDTree(xy).query_pairs(fam['r_coarse'], output_type='ndarray')
        if len(pairs):
            i, j = pairs[:, 0], pairs[:, 1]
            d = np.hypot(*(xy[i]-xy[j]).T).astype(np.float32)
            F.append((i.astype(np.int32)*n + j).astype(np.int32))
            D.append(d); TI.append(np.full(len(i), it, np.int32))
    F = np.concatenate(F); D = np.concatenate(D); TI = np.concatenate(TI)
    order = np.lexsort((D, F))                            # per pair, min-dist entry first
    Fs = F[order]
    first = np.empty(len(Fs), bool); first[0] = True; first[1:] = Fs[1:] != Fs[:-1]
    sel = order[first]
    pi, pj = Fs[first]//n, Fs[first] % n
    pd, pt = D[sel].astype(np.float64), TI[sel]
    # refine each pair around its coarse argmin
    events = []
    CH = 400
    for s in range(0, len(pi), CH):
        c = slice(s, s+CH)
        tt = (pt[c][:, None] + np.linspace(-1.0, 1.0, 129)[None, :])*dt
        ii, jj = pi[c], pj[c]
        def dist(tt, ii, jj):
            Pa = kepler_xy(a[ii][:, None], e[ii][:, None], w[ii][:, None], M0[ii][:, None] + nv[ii][:, None]*tt)
            Pb = kepler_xy(a[jj][:, None], e[jj][:, None], w[jj][:, None], M0[jj][:, None] + nv[jj][:, None]*tt)
            d = np.linalg.norm(Pa-Pb, axis=-1)
            am = d.argmin(axis=1)
            ar = np.arange(d.shape[0])
            return d[ar, am], tt[ar, am]
        d1, t1 = dist(tt, ii, jj)
        # zoom: one more pass at 1/128 of the coarse step around t1
        span = (dt/128)*np.linspace(-1.0, 1.0, 33)[None, :]
        dm, tm = dist(t1[:, None] + span, ii, jj)
        for hit in np.nonzero(dm < R)[0]:
            events.append((int(ii[hit]), int(jj[hit]), float(tm[hit]), float(dm[hit])))
    return events

def analyse(fam, events, name):
    a, M0 = fam['a'], fam['M0']
    nv = np.sqrt(GM/a**3)
    ranks, times = [], []
    tc_cache = {}
    for i, j, tc, _ in events:
        key = round(tc, 9)
        if key not in tc_cache:
            inv = np.empty(len(M0), int); inv[np.argsort((M0+nv*tc) % (2*np.pi), kind='stable')] = np.arange(len(M0))
            tc_cache[key] = inv
        ranks.append(abs(int(tc_cache[key][i]) - int(tc_cache[key][j])))
        times.append(tc)
    rk = np.array(ranks, float)
    e, w, aa = fam['e'], fam['w'], fam['a']
    p = aa*(1-e**2); U, V, W = 1/p, e*np.cos(w)/p, e*np.sin(w)/p
    i0 = rng.choice(len(U), min(4000, len(U)), replace=False)
    dU2 = (U[i0]-U.mean())**2; dT2 = (V[i0]-V.mean())**2 + (W[i0]-W.mean())**2
    res = dict(scenario=name, n=int(len(a)), events=int(len(events)),
               unique_pairs=int(len({(min(i, j), max(i, j)) for i, j, _, _ in events})),
               frac_rank_le_K=round(float((rk <= K).mean()), 4) if len(rk) else None,
               median_rank=float(np.median(rk)) if len(rk) else None,
               p90_rank=float(np.percentile(rk, 90)) if len(rk) else None,
               max_rank=int(rk.max()) if len(rk) else None,
               dU=float(np.sqrt(dU2.mean())), dT=float(np.sqrt(dT2.mean())),
               cone_fraction=float(np.mean(dU2 <= dT2)))
    if name == 'S2 interception':
        half = len(a)//2
        cross = [(i, j, tc, dd) for i, j, tc, dd in events if (i < half) != (j < half)]
        rkc = np.array([abs(int(tc_cache[round(tc, 9)][i]) - int(tc_cache[round(tc, 9)][j]))
                        for i, j, tc, _ in cross], float) if cross else np.array([], float)
        res['cross_events'] = int(len(cross))
        res['cross_frac_rank_le_K'] = round(float((rkc <= K).mean()), 4) if len(rkc) else None
        res['cross_median_rank'] = float(np.median(rkc)) if len(rkc) else None
        res['cross_rank_p10_p90'] = [float(np.percentile(rkc, 10)), float(np.percentile(rkc, 90))] if len(rkc) else None
    if len(rk):
        res['rank_hist'] = {str(q): float(np.percentile(rk, q)) for q in (10, 25, 50, 75, 90)}
    return res

def main():
    t00 = time.time(); out = {}
    for name, fam in [('S0 shear', shear_control()),
                      ('S1 family', collision_family()),
                      ('S2 interception', interception()),
                      ('S4 mixed', mixed_formation())]:
        t0 = time.time()
        ev = find_contacts(fam)
        res = analyse(fam, ev, name); res['seconds'] = round(time.time()-t0, 2)
        out[name] = res
        print(json.dumps(res), flush=True)
    # instrument control: random-pair rank baseline (uniform ordering => ~n/6)
    base = np.abs(rng.integers(0, 500, (4000, 2)).T.astype(int)[0] -
                  rng.integers(0, 500, (4000, 2)).T.astype(int)[1])
    out['instrument_random_pair_median_rank'] = float(np.median(base))
    out.update(R=R, K=K, seed=SEED, total_seconds=round(time.time()-t00, 2))
    json.dump(out, open(sys.path[0]+f'/metrics-R{R:.0e}.json', 'w'), indent=1)
    print('total', out['total_seconds'], 's')

if __name__ == '__main__':
    main()
