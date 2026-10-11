#!/usr/bin/env python3
"""Rotation-certificate probe (library lens, run 20261011-0924-library-9834).

Frozen-element coplanar Keplerian pairs. Strobe at the synodic period Ts:
mean motions are linear, so the configuration at strobe k is the strobe-0
configuration shifted along the torus diagonal by 2*pi*r*k (r = frac(n1*Ts/2pi));
the per-interval minimum distance is D_min(theta_k), theta_k = frac(th0 + r k).
The encounter indicator is a rotation-hitting sequence. Measured per pair:
window arcs W (from observed hits), coverage horizon k_hat (three-gap/CF:
a hit is guaranteed within k_hat intervals), the return-time structure of the
hit sequence (Slater: at most a few distinct gaps), and a fit/test split for
the generator claim. Outputs results.json + pairs.csv next to this file.
"""
import numpy as np, json, time, csv, os

rng = np.random.default_rng(20261011)
K, S = 1024, 48          # synodic intervals, grid samples per interval
NPAIRS = 300
CAP = 300_000            # max coverage q

def kepler(a, e, varpi, M):
    E = M.copy()
    for _ in range(6):
        E -= (E - e*np.sin(E) - M) / (1.0 - e*np.cos(E))
    x = a*(np.cos(E) - e); y = a*np.sqrt(1-e*e)*np.sin(E)
    nu = 2*np.arctan2(np.sqrt(1+e)*np.sin(E/2), np.sqrt(1-e)*np.cos(E/2))
    return x, y, varpi + nu

def sim_pair(a1,e1,w1,m10, a2,e2,w2,m20):
    n1, n2 = a1**-1.5, a2**-1.5
    Ts = 2*np.pi/abs(n1-n2)
    r = float(np.mod(n1*Ts/(2*np.pi), 1.0))
    th0 = float(np.mod(m10/(2*np.pi), 1.0))
    k = np.arange(K, dtype=float)
    d = np.mod((n1-n2)*k*Ts, 2*np.pi)          # exactness: strobe shifts are diagonal
    d = np.minimum(d, 2*np.pi-d)
    assert d.max() < 1e-8, "diagonal strobe invariant violated"
    dt = Ts/S
    t = k[:,None]*Ts + (np.arange(S)[None,:]+0.5)*dt
    x1,y1,l1 = kepler(a1,e1,w1, m10 + n1*t)
    x2,y2,l2 = kepler(a2,e2,w2, m20 + n2*t)
    u = np.mod(l1-l2+np.pi, 2*np.pi) - np.pi          # relative true longitude
    dist = np.hypot(x1-x2, y1-y2)
    dmin = dist.min(axis=1).astype(float)
    m = (u[:, :-1]*u[:, 1:] <= 0) & (u[:, :-1] != u[:, 1:])
    rows, cols = np.nonzero(m)
    if len(rows):
        u0, u1_ = u[rows, cols], u[rows, cols+1]
        tj = rows*Ts + (cols+0.5)*dt
        tc = tj + (u0/(u0-u1_))*dt
        xc1,yc1,_ = kepler(a1,e1,w1, m10 + n1*tc)
        xc2,yc2,_ = kepler(a2,e2,w2, m20 + n2*tc)
        np.minimum.at(dmin, rows, np.hypot(xc1-xc2, yc1-yc2))
    nox = np.setdiff1d(np.arange(K), np.unique(rows))
    if len(nox):
        j = np.abs(u[nox]).argmin(axis=1)
        sel = nox[np.abs(u[nox, j]) < 0.05]
        if len(sel):
            js = np.abs(u[sel]).argmin(axis=1)
            offs = np.linspace(-dt, dt, 9)
            tt = sel[:,None]*Ts + (js[:,None]+0.5)*dt + offs[None,:]
            xf1,yf1,_ = kepler(a1,e1,w1, m10 + n1*tt.ravel())
            xf2,yf2,_ = kepler(a2,e2,w2, m20 + n2*tt.ravel())
            dd = np.hypot(xf1-xf2, yf1-yf2).reshape(len(sel), 9).min(axis=1)
            np.minimum.at(dmin, sel, dd)
    return dmin, r, th0

def cf_cands(r, cap=CAP):
    if r < 1e-12: return [1]
    x, q_prev, q_cur, out = r, 1, 0, []
    for _ in range(80):
        a = int(x // 1)
        q = a*q_cur + q_prev
        if q > cap: break
        if q > 0: out.append(q)
        q_prev, q_cur = q_cur, q
        f = x - a
        if f < 1e-14: break
        x = 1.0/f
    cands = set(out)
    for i in range(len(out)-1): cands.add(out[i]+out[i+1])
    return sorted(cands) if cands else [1]

def horizon(r, th_start, w, cands):
    """Coverage bound: some orbit point within q steps lands in any arc of
    width > maxgap(q), so if maxgap(q) < w a hit occurs within q intervals."""
    if w <= 0: return None
    for q in cands:
        if q > CAP: break
        if q == 1: mg = 1.0
        else:
            ph = np.sort(np.mod(th_start + r*np.arange(q), 1.0))
            mg = max(np.diff(ph).max(), ph[0]+1.0-ph[-1])
        if mg < w: return q
    return None

def arcs_robust(phases, hit, max_gap):
    """Maximal circular arcs of hit phases; consecutive hits separated by more
    than max_gap (the sampling resolution of the phase orbit) break an arc."""
    hp = np.sort(phases[hit])
    if len(hp) == 0: return []
    if len(hp) == 1: return [(hp[0], hp[0])]
    gaps = np.diff(hp)
    wrap = hp[0] + 1.0 - hp[-1]
    allg = np.append(gaps, wrap)
    if (allg > max_gap).sum() == 0:
        i = int(np.argmax(allg))
        start = hp[i+1] if i < len(hp)-1 else hp[0]
        return [(start, start + (1.0 - allg.max()))]
    segs, s0 = [], 0
    for i, g in enumerate(gaps):
        if g > max_gap: segs.append((hp[s0], hp[i])); s0 = i+1
    segs.append((hp[s0], hp[-1]))
    if wrap <= max_gap and len(segs) > 1:
        (a1_, _) = segs[-1]; (_, b2_) = segs[0]
        segs = [(a1_, b2_ + 1.0)] + segs[1:-1]
    return [(a, b) for a, b in segs if b > a]

def inarc(ph, arcs):
    z = np.mod(ph, 1.0)
    inside = np.zeros_like(z, dtype=bool)
    for a, b in arcs:
        if b <= 1.0: inside |= (z >= a) & (z <= b)
        else: inside |= (z >= a) | (z <= b-1.0)
    return inside

def main():
    t0 = time.time()
    pairs = []
    for _ in range(NPAIRS):
        a1 = rng.uniform(0.97, 1.03)
        da = rng.uniform(0.0008, 0.03)*rng.choice([-1, 1])
        a2 = a1 + da
        if not (0.96 < a2 < 1.04): a2 = a1 - da
        pairs.append(dict(a1=a1, e1=rng.uniform(0, 0.08), w1=rng.uniform(0, 2*np.pi),
                          m10=rng.uniform(0, 2*np.pi), a2=a2, e2=rng.uniform(0, 0.08),
                          w2=rng.uniform(0, 2*np.pi), m20=rng.uniform(0, 2*np.pi), tag='rand'))
    pairs.append(dict(a1=1.0, e1=0.0, w1=0.0, m10=0.0, a2=2**(-2/3), e2=0.05, w2=0.3,
                      m20=1.2, tag='resonant-2:1'))   # r=0 exactly: frozen phase
    pairs.append(dict(a1=1.0, e1=0.0, w1=0.0, m10=0.0, a2=1.05, e2=0.0, w2=0.0,
                      m20=0.0, tag='disjoint-radial'))  # provable w=0 forever
    pairs.append(dict(a1=1.0, e1=0.0, w1=0.0, m10=0.0, a2=1.001, e2=0.0, w2=0.0,
                      m20=0.5, tag='overlap-every'))    # w=1: hit every interval

    TH = {'0.005a': 0.005, '0.002a': 0.002}
    recs = []
    for p in pairs:
        dmin, r, th0 = sim_pair(p['a1'],p['e1'],p['w1'],p['m10'], p['a2'],p['e2'],p['w2'],p['m20'])
        phases = np.mod(th0 + r*np.arange(K), 1.0)
        sp = np.sort(phases)
        mg_all = max(np.diff(sp).max(), sp[0]+1.0-sp[-1])
        rec = dict(tag=p['tag'], a1=round(p['a1'],5), a2=round(p['a2'],5),
                   e1=round(p['e1'],4), e2=round(p['e2'],4), r=r,
                   dmin_min=float(dmin.min()), dmin_med=float(np.median(dmin)))
        for name, R in TH.items():
            hits = dmin < R
            hk = np.nonzero(hits)[0]
            gaps = np.diff(hk)
            rec[f'nhits_{name}'] = int(hits.sum())
            # return-time structure (fit on first half of hits, test on second)
            if len(gaps):
                h1 = set(int(g) for g in gaps[:max(1, len(gaps)//2)])
                h2 = [int(g) for g in gaps[max(1, len(gaps)//2):]]
                rec[f'gaps_uniq_{name}'] = sorted(set(int(g) for g in gaps))[:12]
                rec[f'gaps2_cov_{name}'] = (float(np.mean([g in h1 for g in h2])) if h2 else None)
            else:
                rec[f'gaps_uniq_{name}'] = []
                rec[f'gaps2_cov_{name}'] = None
            if r < 1e-12:                       # frozen phase (exact commensurability)
                rec[f'w_{name}'] = 1.0 if hits.all() else 0.0
                rec[f'arcs_{name}'] = 1
                rec[f'khat_{name}'] = 1 if hits.all() else None
                rec[f'viol_{name}'] = 0; rec[f'nchecks_{name}'] = 0
                rec[f'eff_med_{name}'] = None
                rec[f'gap_med_{name}'] = 1 if hits.all() else None
                rec[f'gap_min_{name}'] = 1 if hits.all() else None
                rec[f'p1_mism_{name}'] = 0; rec[f'p1_tot_{name}'] = 0
                continue
            arcs = arcs_robust(phases, hits, mg_all)
            w_est = max((b-a) for a, b in arcs) if arcs else 0.0
            rec[f'w_{name}'] = w_est
            rec[f'arcs_{name}'] = len(arcs)
            # P1: fit arcs on even intervals, test on odd, boundary band excluded
            band = np.abs(dmin - R) < 0.05*R
            ev, od = np.arange(0, K, 2), np.arange(1, K, 2)
            spe = np.sort(phases[ev])
            mg_ev = max(np.diff(spe).max(), spe[0]+1.0-spe[-1])
            arcs_ev = arcs_robust(phases[ev], hits[ev], mg_ev)
            mism = tot = 0
            if arcs_ev:
                sel = ~band[od]
                mism = int((inarc(phases[od][sel], arcs_ev) != hits[od][sel]).sum())
                tot = int(sel.sum())
            rec[f'p1_mism_{name}'] = mism; rec[f'p1_tot_{name}'] = tot
            # P3: rolling coverage bound (theorem check, not a scheduler)
            cands = cf_cands(r)
            viol, effs, nch = 0, [], 0
            if len(hk) and w_est > 0:
                for s, n_ in zip([0]+list(hk[:-1]), list(hk)):
                    kh = horizon(r, phases[s], w_est, cands)
                    if kh is None: continue
                    nch += 1
                    if n_ - s > kh: viol += 1
                    else: effs.append((n_-s)/kh)
            rec[f'viol_{name}'] = viol
            rec[f'nchecks_{name}'] = nch
            rec[f'eff_med_{name}'] = float(np.median(effs)) if effs else None
            rec[f'gap_med_{name}'] = float(np.median(gaps)) if len(gaps) else None
            rec[f'gap_min_{name}'] = float(gaps.min()) if len(gaps) else None
            rec[f'khat_{name}'] = (horizon(r, 0.0, w_est, cands) if w_est > 0 else None)
        recs.append(rec)
        if len(recs) % 50 == 0: print(f'{len(recs)} pairs, {time.time()-t0:.1f}s', flush=True)

    out = {'K': K, 'S': S, 'npairs': len(pairs), 'runtime_s': round(time.time()-t0,1), 'th': {}}
    for name in TH:
        R = [x for x in recs if x['tag'] == 'rand']
        nohit = [x for x in R if x[f'nhits_{name}'] == 0]
        wpos = [x for x in R if x[f'w_{name}'] > 0]
        allviol = sum(x[f'viol_{name}'] for x in R)
        mism = sum(x[f'p1_mism_{name}'] for x in R); tot = sum(x[f'p1_tot_{name}'] for x in R)
        effs = [x[f'eff_med_{name}'] for x in R if x[f'eff_med_{name}'] is not None]
        gm = [x[f'gap_med_{name}'] for x in R if x[f'gap_med_{name}'] is not None]
        mg = [x[f'gap_min_{name}'] for x in R if x[f'gap_min_{name}'] is not None]
        kh = [x[f'khat_{name}'] for x in R if x[f'khat_{name}']]
        Gsafe = min(mg) if mg else None
        gmed = float(np.median(gm)) if gm else None
        g1 = [x for x in R if x[f'gaps_uniq_{name}']]
        sl = [len(x[f'gaps_uniq_{name}']) for x in g1]
        cov2 = [x[f'gaps2_cov_{name}'] for x in g1 if x[f'gaps2_cov_{name}'] is not None]
        out['th'][name] = dict(
            frac_nohit_1024=len(nohit)/len(R),
            frac_w_pos=len(wpos)/len(R),
            p1_mismatch_rate=(mism/tot if tot else None), p1_tested=tot,
            safety_violations=int(allviol),
            eff_median=(float(np.median(effs)) if effs else None), eff_pairs=len(effs),
            gap_median=gmed,
            gap_p99_per_med=(float(np.percentile(gm,99)/np.median(gm)) if len(gm) > 100 else None),
            global_safe_cadence=Gsafe,
            khat_median=(float(np.median(kh)) if kh else None), khat_max=int(max(kh)) if kh else None,
            global_cadence_overhead=(gmed/Gsafe if (Gsafe and gmed) else None),
            slater_le3=(sum(1 for s in sl if s <= 3)/len(sl) if sl else None),
            slater_le5=(sum(1 for s in sl if s <= 5)/len(sl) if sl else None),
            slater_vals=(float(np.median(sl)) if sl else None),
            gaps2_cov_mean=(float(np.mean(cov2)) if cov2 else None),
        )
    ctrl = {x['tag']: {n: dict(w=x[f'w_{n}'], nhits=x[f'nhits_{n}'], viol=x[f'viol_{n}'])
                      for n in TH} for x in recs if x['tag'] != 'rand'}
    out['controls'] = ctrl
    out['pairs'] = recs
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, 'results.json'), 'w') as f: json.dump(out, f, indent=1)
    with open(os.path.join(here, 'pairs.csv'), 'w', newline='') as f:
        wr = csv.DictWriter(f, fieldnames=list(recs[0].keys())); wr.writeheader()
        for r_ in recs: wr.writerow(r_)
    print(json.dumps({'th': out['th'], 'controls': ctrl}, indent=1))

if __name__ == '__main__':
    main()
