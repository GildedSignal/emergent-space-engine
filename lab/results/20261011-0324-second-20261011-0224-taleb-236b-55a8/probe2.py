#!/usr/bin/env python3
"""Second-author probe for run 20261011-0224-taleb-236b: repairs the record
named by the first checker (see work/orig/check.md, "What the author missed").

Subcommands (deterministic, seed 20261011, each <= 60 s):
  conj      S4 conjunction record: pairs whose dM crosses 0 within the horizon,
            exact miss at conjunction, contact x conjunction cross-tab, and the
            rank<=4 tail attribution (crossing offsets of the contacting pairs).
  dense     S4 contact truth with the coarse-capture bias removed (all pairs,
            no KDTree prefilter) at spP 16/64/256 + v_rel at contacts.
  boundary  S5 trigger-boundary case (cone ~0.6), shipped as runnable code.
  prec      the missing experiment: S4 + apsidal precession sweep
            (differential sigma_kappa in {0,1e-3,1e-2,5e-2} rad/orbit plus a
            rigid control), live/frozen rank structure, crossing-offset drift,
            event-rate cost.

Usage: python3 probe2.py <cmd> [R=1e-4]
Fleet generation is byte-identical to probe.py (same rng seed, same draw
order), so S4 here is the author's exact fleet; with kappa=0 the finder path
reproduces the author's events bit for bit.
"""
import json, sys, time
import numpy as np

GM = 1.0
A0 = 1.0
R = float(sys.argv[2]) if len(sys.argv) > 2 else 1e-4   # contact radius
K = 4                                                    # certificate rank
SEED = 20261011
CMD = sys.argv[1]

def kepler_xy(a, e, w, M):
    E = np.asarray(M, float).copy()
    a = np.asarray(a, float); e = np.asarray(e, float); w = np.asarray(w, float)
    for _ in range(14):
        E = E - (E - e*np.sin(E) - M) / (1.0 - e*np.cos(E))
    r = a * (1.0 - e*np.cos(E))
    th = 2.0*np.arctan2(np.sqrt(1.0+e)*np.sin(E/2), np.sqrt(1.0-e)*np.cos(E/2))
    return np.stack([r*np.cos(th+w), r*np.sin(th+w)], axis=-1)

def M_of_theta(theta, e):
    e = np.asarray(e, float)
    E = 2.0*np.arctan2(np.sqrt(1.0-e)*np.sin(theta/2), np.sqrt(1.0+e)*np.cos(theta/2))
    return E - e*np.sin(E)

rng = np.random.default_rng(SEED)

# ------------------------------------------------------------- families
# (verbatim from probe.py; call order must match probe.main to reproduce fleets)
def shear_control(n=500):
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
    a = A0*(1.0 + rng.normal(0, 2e-4, n)); a.sort()
    e = np.clip(0.01 + rng.normal(0, 2e-3, n), 1e-4, None)
    return dict(a=a, e=e, w=rng.normal(0.0, 0.1, n), M0=rng.normal(0.0, 0.06, n),
                periods=24, spP=16, r_coarse=R + 6e-3, frozen=False)

def boundary_case(n=300):
    # checker 1's adversarial case: sigma_a=2e-4, e pinned 0.01, sigma_w=0.03
    a = A0*(1.0 + rng.normal(0, 2e-4, n)); a.sort()
    return dict(a=a, e=np.full(n, 0.01), w=rng.normal(0.0, 0.03, n),
                M0=rng.normal(0.0, 0.06, n), periods=24, spP=16,
                r_coarse=R + 6e-3, frozen=False)

def fleets():
    return {'S0': shear_control(), 'S1': collision_family(),
            'S2': interception(), 'S4': mixed_formation()}

# ------------------------------------------------------------- truth
def find_contacts2(fam, kappa=None, all_pairs=False, spP=None, r_all=None):
    """probe.find_contacts + per-ship apsidal precession (kappa, rad/orbit)
    and an all-pairs mode that removes the KDTree coarse-capture bias."""
    a, e, w, M0 = fam['a'], fam['e'], fam['w'], fam['M0']
    n = len(a); nv = np.sqrt(GM/a**3)
    n0 = nv.mean()
    sp = fam['spP'] if spP is None else spP
    T = fam['periods']*sp
    dt = (2*np.pi/n0)/sp
    krate = (np.zeros(n) if kappa is None else np.asarray(kappa)*nv/(2*np.pi))
    thr = (r_all if all_pairs else fam['r_coarse'])
    F, D, TI = [], [], []
    iu, ju = np.triu_indices(n, 1)
    for it in range(T):
        t = (it+0.5)*dt
        xy = kepler_xy(a, e, w + krate*t, M0 + nv*t)
        if all_pairs:
            d = np.hypot(xy[iu, 0]-xy[ju, 0], xy[iu, 1]-xy[ju, 1]).astype(np.float32)
            m = d < thr
            if m.any():
                F.append((iu[m].astype(np.int32)*n + ju[m]).astype(np.int32))
                D.append(d[m]); TI.append(np.full(int(m.sum()), it, np.int32))
        else:
            from scipy.spatial import cKDTree
            pairs = cKDTree(xy).query_pairs(fam['r_coarse'], output_type='ndarray')
            if len(pairs):
                i, j = pairs[:, 0], pairs[:, 1]
                d = np.hypot(*(xy[i]-xy[j]).T).astype(np.float32)
                F.append((i.astype(np.int32)*n + j).astype(np.int32))
                D.append(d); TI.append(np.full(len(i), it, np.int32))
    F = np.concatenate(F); D = np.concatenate(D); TI = np.concatenate(TI)
    order = np.lexsort((D, F))
    Fs = F[order]
    first = np.empty(len(Fs), bool); first[0] = True; first[1:] = Fs[1:] != Fs[:-1]
    sel = order[first]
    pi, pj = Fs[first]//n, Fs[first] % n
    pt = TI[sel]
    events = []
    CH = 400
    for s in range(0, len(pi), CH):
        c = slice(s, s+CH)
        tt = (pt[c][:, None] + np.linspace(-1.0, 1.0, 129)[None, :])*dt
        ii, jj = pi[c], pj[c]
        def dist(tt, ii, jj):
            Pa = kepler_xy(a[ii][:, None], e[ii][:, None],
                           w[ii][:, None] + krate[ii][:, None]*tt,
                           M0[ii][:, None] + nv[ii][:, None]*tt)
            Pb = kepler_xy(a[jj][:, None], e[jj][:, None],
                           w[jj][:, None] + krate[jj][:, None]*tt,
                           M0[jj][:, None] + nv[jj][:, None]*tt)
            d = np.linalg.norm(Pa-Pb, axis=-1)
            am = d.argmin(axis=1); ar = np.arange(d.shape[0])
            return d[ar, am], tt[ar, am]
        d1, t1 = dist(tt, ii, jj)
        span = (dt/128)*np.linspace(-1.0, 1.0, 33)[None, :]
        dm, tm = dist(t1[:, None] + span, ii, jj)
        for hit in np.nonzero(dm < R)[0]:
            events.append((int(ii[hit]), int(jj[hit]), float(tm[hit]), float(dm[hit])))
    return events

# ------------------------------------------------------------- instruments
def ordering_inv(M):
    inv = np.empty(len(M), int)
    inv[np.argsort(M % (2*np.pi), kind='stable')] = np.arange(len(M))
    return inv

def cone_fraction(fam):
    a, e, w = fam['a'], fam['e'], fam['w']
    p = a*(1-e**2); U, V, W = 1/p, e*np.cos(w)/p, e*np.sin(w)/p
    dU2 = (U-U.mean())**2; dT2 = (V-V.mean())**2 + (W-W.mean())**2
    return float(np.mean(dU2 <= dT2))

def rank_arrays(fam, events, kappa=None):
    """live M-rank, frozen(t=0) M-rank, live mean-longitude rank per event."""
    a, e, w, M0 = fam['a'], fam['e'], fam['w'], fam['M0']
    n = len(a); nv = np.sqrt(GM/a**3)
    krate = (np.zeros(n) if kappa is None else np.asarray(kappa)*nv/(2*np.pi))
    inv0 = ordering_inv(M0)
    cache = {}
    rl, rf, rlam = [], [], []
    for i, j, tc, _ in events:
        key = round(tc, 9)
        if key not in cache:
            cache[key] = ordering_inv(M0 + nv*tc)
        inv = cache[key]
        rl.append(abs(int(inv[i]) - int(inv[j])))
        rf.append(abs(int(inv0[i]) - int(inv0[j])))
        lam = (M0 + nv*tc + w + krate*tc) % (2*np.pi)
        il = ordering_inv(lam)
        rlam.append(abs(int(il[i]) - int(il[j])))
    return np.array(rl), np.array(rf), np.array(rlam)

def crossing_dM(fam, krate, ii, jj, tt):
    """crossing offset dM* = M_i - M_j at the orbit-crossing longitude nearest
    each event's contact position, for ellipses at times tt (precessing)."""
    a, e, w = fam['a'], fam['e'], fam['w']
    p_i = a[ii]*(1-e[ii]**2); p_j = a[jj]*(1-e[jj]**2)
    wi = w[ii] + krate[ii]*tt; wj = w[jj] + krate[jj]*tt
    A = p_i*e[jj]*np.cos(wj) - p_j*e[ii]*np.cos(wi)
    B = p_i*e[jj]*np.sin(wj) - p_j*e[ii]*np.sin(wi)
    C = p_i - p_j
    Rh = np.hypot(A, B); ph = np.arctan2(B, A)
    degenerate = Rh < 1e-12
    x = np.clip(np.where(degenerate, 1.0, -C/np.where(degenerate, 1.0, Rh)), -1, 1)
    th1 = ph + np.arccos(x); th2 = ph - np.arccos(x)
    def Mat(th, ek, wk):
        nu = th - wk
        E = 2.0*np.arctan2(np.sqrt(1.0-ek)*np.sin(nu/2), np.sqrt(1.0+ek)*np.cos(nu/2))
        return E - ek*np.sin(E)
    dM1 = Mat(th1, e[ii], wi) - Mat(th1, e[jj], wj)
    dM2 = Mat(th2, e[ii], wi) - Mat(th2, e[jj], wj)
    nv = np.sqrt(GM/a**3); M0 = fam['M0']
    xy = kepler_xy(a[ii], e[ii], wi, M0[ii] + nv[ii]*tt)
    th_c = np.arctan2(xy[:, 1], xy[:, 0])
    def wrap(x):
        return (x + np.pi) % (2*np.pi) - np.pi
    pick1 = np.abs(wrap(th1 - th_c)) <= np.abs(wrap(th2 - th_c))
    dM = np.where(pick1, dM1, dM2)
    return np.where(degenerate, 0.0, wrap(dM))

def summarize(fam, events, kappa=None):
    rl, rf, rlam = rank_arrays(fam, events, kappa)
    res = dict(events=len(events),
               unique_pairs=len({(min(i, j), max(i, j)) for i, j, _, _ in events}),
               frac_rank_le_K=round(float((rl <= K).mean()), 4) if len(rl) else None,
               median_rank=float(np.median(rl)) if len(rl) else None,
               p90_rank=float(np.percentile(rl, 90)) if len(rl) else None,
               max_rank=int(rl.max()) if len(rl) else None,
               frozen_frac_rank_le_K=round(float((rf <= K).mean()), 4) if len(rf) else None,
               lambda_frac_rank_le_K=round(float((rlam <= K).mean()), 4) if len(rlam) else None,
               lambda_median_rank=float(np.median(rlam)) if len(rlam) else None)
    return res, rl, rf

def v_rel_at(fam, events, kappa=None):
    a, e, w, M0 = fam['a'], fam['e'], fam['w'], fam['M0']
    nv = np.sqrt(GM/a**3)
    krate = (np.zeros(len(a)) if kappa is None else np.asarray(kappa)*nv/(2*np.pi))
    ii = np.array([ev[0] for ev in events]); jj = np.array([ev[1] for ev in events])
    tt = np.array([ev[2] for ev in events])
    def pos(b, t):
        return kepler_xy(a[b], e[b], w[b] + krate[b]*t, M0[b] + nv[b]*t)
    h = 1e-5
    v = np.linalg.norm(((pos(ii, tt+h)-pos(ii, tt-h)) -
                        (pos(jj, tt+h)-pos(jj, tt-h)))/(2*h), axis=-1)
    return v

# ------------------------------------------------------------- subcommands
def cmd_conj():
    fam = fleets()['S4']
    a, e, w, M0 = fam['a'], fam['e'], fam['w'], fam['M0']
    n = len(a); nv = np.sqrt(GM/a**3); n0 = nv.mean()
    T_end = fam['periods']*(2*np.pi/n0)
    iu, ju = np.triu_indices(n, 1)
    dM0 = M0[ju] - M0[iu]; dn = nv[ju] - nv[iu]
    assert np.abs(dM0).max() + np.abs(dn).max()*T_end < np.pi, "dM wraps 2pi"
    with np.errstate(divide='ignore', invalid='ignore'):
        tc = np.where(dn != 0, -dM0/np.where(dn == 0, 1.0, dn), np.inf)
    m = (dn != 0) & (tc >= 0) & (tc <= T_end)
    ip, jp, tcc = iu[m], ju[m], tc[m]
    Pa = kepler_xy(a[ip], e[ip], w[ip], M0[ip] + nv[ip]*tcc)
    Pb = kepler_xy(a[jp], e[jp], w[jp], M0[jp] + nv[jp]*tcc)
    miss = np.linalg.norm(Pa-Pb, axis=-1)
    out = dict(conj_pairs=int(m.sum()),
               conj_miss_min=float(miss.min()), conj_miss_median=float(np.median(miss)),
               conj_miss_max=float(miss.max()),
               conj_miss_lt_R_1e4=int((miss < 1e-4).sum()),
               conj_miss_lt_R_3e4=int((miss < 3e-4).sum()),
               conj_miss_pcts={str(q): float(np.percentile(miss, q))
                               for q in (1, 5, 10, 50, 90, 99)})
    # contact truth without capture bias
    ev = find_contacts2(fam, all_pairs=True, spP=64, r_all=R + 6e-3)
    cset = {(min(i, j), max(i, j)) for i, j, _, _ in ev}
    conj_set = {(int(i), int(j)) for i, j in zip(ip, jp)}
    inter = [p for p in cset if p in conj_set]
    imiss = {p: float(miss[(ip == p[0]) & (jp == p[1])][0]) for p in inter}
    out.update(dense_events=len(ev), contact_conj_pairs=len(inter),
               contact_conj_miss_min=float(min(imiss.values())) if inter else None,
               contact_conj_miss_max=float(max(imiss.values())) if inter else None,
               author_59_candidates={
                   'contact_conj_in_0p02_0p33': int(sum(1 for v in imiss.values() if 0.02 <= v <= 0.33)),
                   'conj_pairs_miss_in_0p02_0p33': int(((miss >= 0.02) & (miss <= 0.33)).sum())})
    # rank instrument + tail attribution
    res, rl, rf = summarize(fam, ev)
    out['dense'] = res
    ii = np.array([x[0] for x in ev]); jj = np.array([x[1] for x in ev])
    tt = np.array([x[2] for x in ev])
    alloff = crossing_dM(fam, np.zeros(n), ii, jj, tt)
    dw_pairs = np.abs(w[iu] - w[ju]); de_pairs = np.abs(e[iu] - e[ju])
    def pct(x, ref):
        return float((ref < x).mean())
    tailmask = rl <= K
    tail_dw = np.abs(w[ii[tailmask]] - w[jj[tailmask]])
    tail_de = np.abs(e[ii[tailmask]] - e[jj[tailmask]])
    tail_off = np.abs(alloff[tailmask])
    tail_dw_pct = np.array([pct(v, dw_pairs) for v in tail_dw])
    out['tail'] = dict(count=int(tailmask.sum()),
                       dMstar_abs_max=float(tail_off.max()) if tailmask.any() else None,
                       dMstar_abs_median=float(np.median(tail_off)) if tailmask.any() else None,
                       pair_dw_below_tail_dw_frac_median=float(np.median(tail_dw_pct)) if tailmask.any() else None,
                       pair_dw_below_tail_dw_frac_max=float(tail_dw_pct.max()) if tailmask.any() else None,
                       dw_max=float(tail_dw.max()) if tailmask.any() else None,
                       de_max=float(tail_de.max()) if tailmask.any() else None,
                       dw_pair_p05=float(np.percentile(dw_pairs, 5)),
                       de_pair_p05=float(np.percentile(de_pairs, 5)))
    out['dM_at_contact_vs_dMstar_p50_absdiff'] = float(np.median(np.abs(
        ((M0[ii] + nv[ii]*tt) - (M0[jj] + nv[jj]*tt)) - alloff)))
    out['v_rel_pct'] = {str(q): float(np.percentile(v_rel_at(fam, ev), q))
                        for q in (50, 90, 95, 99, 100)}
    out['T_end'] = T_end
    return out

def cmd_dense():
    fam = fleets()['S4']
    out = {}
    ev_f = find_contacts2(fam)   # finder, spP=16: must reproduce the author's 871
    out['finder_spP16'] = summarize(fam, ev_f)[0]
    evs = {}
    for sp, thr in ((16, R + 6e-3), (64, R + 6e-3), (256, R + 8e-3)):
        t0 = time.time()
        ev = find_contacts2(fam, all_pairs=True, spP=sp, r_all=thr)
        evs[sp] = ev
        res, rl, _ = summarize(fam, ev)
        res['seconds'] = round(time.time()-t0, 2)
        out[f'allpairs_spP{sp}'] = res
    s256 = {(min(i, j), max(i, j)) for i, j, _, _ in evs[256]}
    for sp in (16, 64):
        s = {(min(i, j), max(i, j)) for i, j, _, _ in evs[sp]}
        out[f'allpairs{sp}_missed_vs_256'] = len(s256 - s)
    out['finder16_missed_vs_256'] = len(s256 - {(min(i, j), max(i, j)) for i, j, _, _ in ev_f})
    return out

def cmd_boundary():
    fam = fleets()['S4']  # keep draw order; boundary drawn after
    b = boundary_case()
    out = dict(cone_fraction=cone_fraction(b), S4_cone_fraction=cone_fraction(fam))
    for mode, kw in (('finder', {}), ('allpairs', dict(all_pairs=True, spP=64, r_all=R+6e-3))):
        ev = find_contacts2(b, **kw)
        res, rl, _ = summarize(b, ev)
        out[mode] = res
    return out

def cmd_prec():
    fam = fleets()['S4']
    n = len(fam['a'])
    nv = np.sqrt(GM/fam['a']**3)
    out = dict(cone_fraction=cone_fraction(fam))
    horizon_orbits = fam['periods']
    rigid = 5e-2*(nv.mean()/nv)   # equal angular rate for all ships
    for label, kappa in (('k0', None),
                         ('sk1e-3', rng.normal(0, 1e-3, n)),
                         ('sk1e-2', rng.normal(0, 1e-2, n)),
                         ('sk5e-2', rng.normal(0, 5e-2, n)),
                         ('rigid5e-2', rigid)):
        t0 = time.time()
        ev = find_contacts2(fam, kappa=kappa)
        res, rl, rf = summarize(fam, ev, kappa=kappa)
        res['seconds'] = round(time.time()-t0, 2)
        res['events_per_body_per_orbit'] = round(len(ev)/(n*horizon_orbits), 5)
        if ev:
            ii = np.array([x[0] for x in ev]); jj = np.array([x[1] for x in ev])
            tt = np.array([x[2] for x in ev])
            krate = (np.zeros(n) if kappa is None else np.asarray(kappa)*nv/(2*np.pi))
            dms_t = crossing_dM(fam, krate, ii, jj, tt)
            dms_0 = crossing_dM(fam, krate, ii, jj, np.zeros_like(tt))
            drift = dms_t - dms_0
            pred = (krate[ii]-krate[jj])*tt     # d(dM*)/dt ~ d(dw)/dt
            res['offset_drift_abs_median'] = float(np.median(np.abs(drift)))
            res['offset_drift_pred_abs_median'] = float(np.median(np.abs(pred)))
            ok = np.abs(pred) > 1e-9
            if ok.sum() > 10:
                res['offset_drift_slope_vs_dkappa_t'] = round(
                    float(np.sum(drift[ok]*pred[ok])/np.sum(pred[ok]**2)), 3)
            dM_at = (fam['M0'][ii] + nv[ii]*tt) - (fam['M0'][jj] + nv[jj]*tt)
            res['dM_at_contact_vs_dMstar_p50_absdiff'] = float(np.median(np.abs(
                (dM_at - dms_t + np.pi) % (2*np.pi) - np.pi)))
        out[label] = res
        print(label, json.dumps(res), flush=True)
    return out

if __name__ == '__main__':
    t0 = time.time()
    out = dict(R=R, K=K, seed=SEED, cmd=CMD)
    out['result'] = globals()[f'cmd_{CMD}']()
    out['total_seconds'] = round(time.time()-t0, 2)
    fn = f'{sys.path[0]}/probe2-{CMD}-R{R:.0e}.json'
    json.dump(out, open(fn, 'w'), indent=1)
    print('wrote', fn, out['total_seconds'], 's')
