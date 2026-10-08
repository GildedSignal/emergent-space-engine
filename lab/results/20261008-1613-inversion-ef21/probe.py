#!/usr/bin/env python3
"""Inversion probe: does the co-orbital phase-neighbour certificate (rank<=4) survive
periapsis dispersion? Exact analytic Kepler truth (no integrator), independent of
crates/encounters (different harness on purpose).

Scenes: TRAIN (gold's formation shape, positive control), RING (attack: e/varpi spread),
RING_MILD, RING_BUNCH (held-out), BELT (negative control, certificate must not apply).
Usage: probe.py [--validate]
"""
import json, sys, time
import numpy as np

TWOPI = 2 * np.pi

def wrap2pi(x): return np.mod(x, TWOPI)
def wrap_pi(x): return np.angle(np.exp(1j * x))
def mean_motion(a): return a ** -1.5

def kepler_E(M, e, iters=8):
    E = M + e * np.sin(M)
    for _ in range(iters):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E

def state_from_M(a, e, varpi, M0, n, t):
    """a,e,varpi,M0,n: leading dims broadcast against t's leading dim(s)."""
    M = wrap2pi(M0 + n * t)
    E = kepler_E(M, e)
    r = a * (1 - e * np.cos(E))
    f = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
    th = varpi + f
    x, y = r * np.cos(th), r * np.sin(th)
    k = n * a / np.sqrt(1 - e * e)
    xo, yo = -k * np.sin(E), k * (np.cos(E) - e)
    c, s = np.cos(varpi), np.sin(varpi)
    return x, y, c * xo - s * yo, s * xo + c * yo

def pair_states(a, e, varpi, M0, n, ii, jj, tt):
    """Positions of bodies ii and jj at times tt (C,) or (C,K)."""
    ii = np.asarray(ii); jj = np.asarray(jj); tt = np.asarray(tt, float)
    ex = (lambda x: np.expand_dims(x, -1)) if tt.ndim == 2 else (lambda x: x)
    x1, y1, _, _ = state_from_M(ex(a[ii]), ex(e[ii]), ex(varpi[ii]), ex(M0[ii]), ex(n[ii]), tt)
    x2, y2, _, _ = state_from_M(ex(a[jj]), ex(e[jj]), ex(varpi[jj]), ex(M0[jj]), ex(n[jj]), tt)
    return x1, y1, x2, y2

def mean_longitudes(a, e, varpi, M0, n, t):
    return wrap2pi(varpi + wrap2pi(M0 + n * t))

def radius_at_theta(e, p, theta, varpi):
    return p / (1 + e * np.cos(theta - varpi))

def make_scene(name, n, seed):
    rng = np.random.default_rng(seed)
    if name == "TRAIN":
        a = rng.normal(1.0, 1e-2, n); e = np.full(n, 0.3)
        varpi = np.zeros(n); M0 = rng.uniform(0, TWOPI, n)
    elif name == "RING":
        a = rng.normal(1.0, 1e-2, n); e = rng.uniform(0.2, 0.4, n)
        varpi = rng.uniform(0, TWOPI, n); M0 = rng.uniform(0, TWOPI, n)
    elif name == "RING_TIGHT":
        a = rng.normal(1.0, 1e-3, n); e = rng.uniform(0.2, 0.4, n)
        varpi = rng.uniform(0, TWOPI, n); M0 = rng.uniform(0, TWOPI, n)
    elif name == "RING_MILD":
        a = rng.normal(1.0, 1e-2, n); e = rng.uniform(0.02, 0.06, n)
        varpi = rng.uniform(0, TWOPI, n); M0 = rng.uniform(0, TWOPI, n)
    elif name == "RING_BUNCH":
        a = rng.normal(1.0, 1e-2, n); e = rng.uniform(0.2, 0.4, n)
        varpi = rng.uniform(0, TWOPI, n); M0 = rng.uniform(0, np.pi / 6, n)
    elif name == "BELT":
        a = rng.uniform(0.7, 1.3, n); e = rng.uniform(0.0, 0.4, n)
        varpi = rng.uniform(0, TWOPI, n); M0 = rng.uniform(0, TWOPI, n)
    elif name == "VALID":  # mixed small scene for brute-force cross-check
        a = rng.normal(1.0, 1e-2, n); e = rng.uniform(0.05, 0.35, n)
        varpi = rng.uniform(0, TWOPI, n); M0 = rng.uniform(0, TWOPI, n)
    else:
        raise ValueError(name)
    return a, e, varpi, M0

def refine_min(a, e, varpi, M0, n, ii, jj, t_c, W):
    """Zoom on min pair distance; 3-stage grid + parabolic. Returns (t_min, d_min)."""
    ii = np.asarray(ii); jj = np.asarray(jj)
    t_c = np.asarray(t_c, float); W = np.asarray(W, float)
    if ii.size == 0:
        return t_c, np.full(0, np.inf)
    best_d = np.full(ii.size, np.inf); best_t = t_c.copy()
    for npts, frac in ((31, 1.0), (21, 0.18), (13, 0.25)):
        tt = t_c[:, None] + np.linspace(-1, 1, npts)[None, :] * (W[:, None] * frac)
        x1, y1, x2, y2 = pair_states(a, e, varpi, M0, n, ii, jj, tt)
        d2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        k = np.clip(np.argmin(d2, axis=1), 1, npts - 2)
        rows = np.arange(ii.size)
        d = np.sqrt(d2[rows, k])
        dl, d0, dr = d2[rows, k - 1], d2[rows, k], d2[rows, k + 1]
        denom = dl - 2 * d0 + dr
        safe = np.abs(denom) > 1e-300
        shift = np.zeros(ii.size)
        shift[safe] = np.clip(0.5 * (dl[safe] - dr[safe]) / denom[safe], -1, 1)
        h = (tt[rows, k + 1] - tt[rows, k - 1]) / 2
        t_par = tt[rows, k] + shift * h
        x1p, y1p, x2p, y2p = pair_states(a, e, varpi, M0, n, ii, jj, t_par)
        d_par = np.sqrt((x1p - x2p) ** 2 + (y1p - y2p) ** 2)
        take = d_par < d
        best_d = np.where(take, d_par, d)
        best_t = np.where(take, t_par, tt[rows, k])
        t_c = best_t.copy(); W = np.maximum(W * frac * 0.2, 1e-9)
    return best_t, best_d

def arrival_base(e, varpi, M0, n, th):
    f = wrap_pi(th - varpi)
    E = 2 * np.arctan2(np.sqrt(1 - e) * np.sin(f / 2), np.sqrt(1 + e) * np.cos(f / 2))
    Mstar = wrap2pi(E - e * np.sin(E))
    return wrap2pi(Mstar - M0) / n, E

def arrival_candidates(a, e, varpi, M0, nn, P, ii, jj, th, T, cut):
    """Both ships pass th once per period; keep near-coincident arrival pairs."""
    b_i, E_i = arrival_base(e[ii], varpi[ii], M0[ii], nn[ii], th)
    b_j, E_j = arrival_base(e[jj], varpi[jj], M0[jj], nn[jj], th)
    k_i = nn[ii] * a[ii] / np.sqrt(1 - e[ii] ** 2)
    k_j = nn[jj] * a[jj] / np.sqrt(1 - e[jj] ** 2)
    vmax = np.maximum(
        k_i * np.sqrt(np.sin(E_i) ** 2 + (np.cos(E_i) - e[ii]) ** 2),
        k_j * np.sqrt(np.sin(E_j) ** 2 + (np.cos(E_j) - e[jj]) ** 2))
    Kmax = int(np.ceil(T / P[ii].min())) + 2
    kk = np.arange(Kmax)
    t_i = b_i[:, None] + kk[None, :] * P[ii][:, None]
    ridx, cidx = np.where(t_i <= T + P[ii].min() * 0.5)
    gi, gj = ii[ridx], jj[ridx]
    ti = t_i[ridx, cidx]
    tj = b_j[ridx] + P[gj] * np.round((ti - b_j[ridx]) / P[gj])
    dtau = ti - tj
    sel = np.abs(dtau) * vmax[ridx] < cut
    return gi[sel], gj[sel], ((ti + tj) / 2)[sel], (np.abs(dtau)[sel] + 0.02)

def find_contacts(a, e, varpi, M0, T, cut, ntheta=257, chunk=20000, verbose=True):
    """Sieve: (1) radial-profile minima per pair (crossings+tangencies) with arrival
    coincidences; (2) mean-longitude conjunctions. Refine, dedupe."""
    n = a.size
    nn = mean_motion(a); P = TWOPI / nn; p = a * (1 - e * e)
    I, J = np.triu_indices(n, 1)
    C_I, C_J, C_T, C_W, C_Y = [], [], [], [], []
    thetas = np.linspace(0, TWOPI, ntheta, endpoint=False)

    for c0 in range(0, I.size, chunk):
        ic, jc = I[c0:c0 + chunk], J[c0:c0 + chunk]
        ri = radius_at_theta(e[ic][:, None], p[ic][:, None], thetas[None, :], varpi[ic][:, None])
        rj = radius_at_theta(e[jc][:, None], p[jc][:, None], thetas[None, :], varpi[jc][:, None])
        g = np.abs(ri - rj)
        loc = np.zeros_like(g, bool)
        loc[:, 1:-1] = (g[:, 1:-1] <= g[:, :-2]) & (g[:, 1:-1] <= g[:, 2:])
        loc[:, 0] = (g[:, 0] <= g[:, -1]) & (g[:, 0] <= g[:, 1])
        loc[:, -1] = (g[:, -1] <= g[:, -2]) & (g[:, -1] <= g[:, 0])
        gmask = np.where(loc, g, np.inf)
        gm = gmask.min(axis=1)
        sub = np.where(gm < cut)[0]
        if sub.size:
            gg = gmask[sub]
            k1 = np.argmin(gg, axis=1)
            gg2 = gg.copy(); gg2[np.arange(sub.size), k1] = np.inf
            k2 = np.argmin(gg2, axis=1)
            for karr in (k1, k2):
                good = gmask[sub, karr] < cut
                if not np.any(good): continue
                si = sub[good]; th = thetas[karr[good]]
                gi, gj, tt, WW = arrival_candidates(
                    a, e, varpi, M0, nn, P, ic[si], jc[si], th, T, cut)
                if gi.size:
                    C_I.append(gi); C_J.append(gj); C_T.append(tt); C_W.append(WW)
                    C_Y.append(np.full(gi.size, 1))
        # family 2: mean-longitude conjunctions
        dn = nn[ic] - nn[jc]
        lam0 = wrap2pi(varpi[ic] + M0[ic] - varpi[jc] - M0[jc])
        si = np.where(np.abs(dn) > 1e-12)[0]
        if si.size:
            ii, jj = ic[si], jc[si]
            dnv = np.abs(dn[si]); lam0v = lam0[si]
            nmax = int(np.ceil(dnv.max() * T / TWOPI)) + 1
            mm = np.arange(nmax + 1)
            # alignment lam0 + dn*t = 2*pi*m; sign matters for the first solution
            off = np.where(dn[si] > 0, TWOPI - lam0v, lam0v)
            t_al = (off[:, None] + TWOPI * mm[None, :]) / dnv[:, None]
            ridx, cidx = np.where(t_al <= T)
            tt = t_al[ridx, cidx]
            gi, gj = ii[ridx], jj[ridx]
            ts = tt[:, None] + np.linspace(-0.3, 0.3, 9)[None, :]
            x1, y1, x2, y2 = pair_states(a, e, varpi, M0, nn, gi, gj, ts)
            d = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2).min(axis=1)
            keep = d < 0.6 * cut
            if np.any(keep):
                C_I.append(gi[keep]); C_J.append(gj[keep])
                C_T.append(tt[keep]); C_W.append(np.full(keep.sum(), 0.3))
                C_Y.append(np.full(keep.sum(), 2))
        if verbose and (c0 // chunk) % 3 == 0:
            print(f"  sieve {c0}/{I.size}: cand {sum(x.size for x in C_I)}", flush=True)
        # family 3: initial proximity (approach in progress at t=0)
        x1, y1, x2, y2 = pair_states(a, e, varpi, M0, nn, ic, jc, np.zeros(ic.size))
        d0 = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        k3 = np.where(d0 < cut)[0]
        if k3.size:
            C_I.append(ic[k3]); C_J.append(jc[k3])
            C_T.append(np.zeros(k3.size)); C_W.append(np.full(k3.size, 0.5))
            C_Y.append(np.full(k3.size, 3))

    if not C_I:
        return (np.array([], int), np.array([], int), np.array([]),
                np.array([]), np.array([], int))
    ci = np.concatenate(C_I); cj = np.concatenate(C_J)
    ct = np.concatenate(C_T); cW = np.concatenate(C_W); cty = np.concatenate(C_Y)
    order = np.lexsort((ct, cj, ci))
    ci, cj, ct, cW, cty = ci[order], cj[order], ct[order], cW[order], cty[order]
    same = (ci[1:] == ci[:-1]) & (cj[1:] == cj[:-1]) & (np.abs(ct[1:] - ct[:-1]) < 0.02)
    gid = np.concatenate([[0], np.cumsum(~same)])
    order2 = np.lexsort((cW, gid))
    ci, cj, ct, cW, cty = ci[order2], cj[order2], ct[order2], cW[order2], cty[order2]
    keep = np.concatenate([[True], gid[order2][1:] != gid[order2][:-1]])
    ci, cj, ct, cW, cty = ci[keep], cj[keep], ct[keep], cW[keep], cty[keep]
    out_t, out_d = [], []
    B = 50000
    for s in range(0, ci.size, B):
        t1, d1 = refine_min(a, e, varpi, M0, nn, ci[s:s + B], cj[s:s + B], ct[s:s + B], cW[s:s + B])
        out_t.append(t1); out_d.append(d1)
    rt = np.concatenate(out_t); rd = np.concatenate(out_d)
    # dedupe: same pair, |t1-t2|<0.02 -> one event, keep smallest d
    order = np.lexsort((rd, rt, cj, ci))
    ci, cj, rt, rd, cty = ci[order], cj[order], rt[order], rd[order], cty[order]
    same = (ci[1:] == ci[:-1]) & (cj[1:] == cj[:-1]) & (np.abs(rt[1:] - rt[:-1]) < 0.02)
    gid = np.concatenate([[0], np.cumsum(~same)])
    order2 = np.lexsort((rd, gid))
    ci, cj, rt, rd, cty = ci[order2], cj[order2], rt[order2], rd[order2], cty[order2]
    first = np.concatenate([[True], gid[order2][1:] != gid[order2][:-1]])
    sel = first & (rt >= 0) & (rt <= T)
    return ci[sel], cj[sel], rt[sel], rd[sel], cty[sel]

def ranks_at(a, e, varpi, M0, n, t, ci, cj):
    lam = mean_longitudes(a, e, varpi, M0, mean_motion(a), t)
    pos = np.empty(n, int); pos[np.argsort(lam, kind="stable")] = np.arange(n)
    return np.abs(pos[ci] - pos[cj])
def run_scene(name, n, seed, T_orbits, bs, out):
    a, e, varpi, M0 = make_scene(name, n, seed)
    nn = mean_motion(a)
    T = T_orbits * TWOPI
    t0 = time.time()
    ci, cj, ct, cd, cty = find_contacts(a, e, varpi, M0, T, cut=50 * max(bs))
    sieve_s = time.time() - t0
    res = {"scene": name, "n": n, "seed": seed, "T_orbits": T_orbits,
           "sieve_s": round(sieve_s, 1), "candidates": int(ci.size),
           "dn_over_n_half_range": float((nn.max() - nn.min()) / 2),
           "sigma_a_over_a": float(np.std(a)), "e_mean": float(np.mean(e))}
    for b in bs:
        sel = np.where(cd < b)[0]
        r_ct = np.empty(sel.size); r_t0 = np.empty(sel.size); typ = cty[sel]
        for q, cidx in enumerate(sel):
            r_ct[q] = ranks_at(a, e, varpi, M0, n, ct[cidx], np.array([ci[cidx]]), np.array([cj[cidx]]))[0]
            r_t0[q] = ranks_at(a, e, varpi, M0, n, 0.0, np.array([ci[cidx]]), np.array([cj[cidx]]))[0]
        ok = r_ct.size > 0
        res[f"b={b}"] = {
            "contacts": int(sel.size),
            "by_type": {"radial_min": int((typ == 1).sum()), "conjunction": int((typ == 2).sum())},
            "median_rank_contact": float(np.median(r_ct)) if ok else None,
            "p90_rank_contact": float(np.percentile(r_ct, 90)) if ok else None,
            "max_rank_contact": int(r_ct.max()) if ok else None,
            "miss_k4_pct": float(100 * np.mean(r_ct > 4)) if ok else None,
            "miss_k16_pct": float(100 * np.mean(r_ct > 16)) if ok else None,
            "miss_k64_pct": float(100 * np.mean(r_ct > 64)) if ok else None,
            "miss_k4_t0_pct": float(100 * np.mean(r_t0 > 4)) if ok else None,
            "k_for_zero_miss": int(r_ct.max()) if ok else None,
        }
    out.append(res)
    print(json.dumps(res, indent=1), flush=True)

def validate(n=48, seed=99, T_orbits=20, b=5e-3):
    """Brute-force all-pairs grid vs the sieve. Independent truth (dense sampling)."""
    a, e, varpi, M0 = make_scene("VALID", n, seed)
    nn = mean_motion(a)
    T = T_orbits * TWOPI
    dt = 4e-3
    steps = int(T / dt)
    I, J = np.triu_indices(n, 1)
    dmin = np.full(I.size, np.inf); tmin = np.zeros(I.size)
    for s0 in range(0, steps, 500):
        tt = np.arange(s0, min(s0 + 500, steps)) * dt
        xx, yy, _, _ = state_from_M(a, e, varpi, M0, nn, tt[:, None])
        d2 = (xx[:, I] - xx[:, J]) ** 2 + (yy[:, I] - yy[:, J]) ** 2
        k = d2.argmin(axis=0)
        rows = np.arange(I.size)
        dmin_new = np.sqrt(d2[k, rows])
        better = dmin_new < dmin
        dmin = np.where(better, dmin_new, dmin)
        tmin = np.where(better, tt[k], tmin)
    ci, cj, ct, cd, _ = find_contacts(a, e, varpi, M0, T, cut=50 * b, verbose=False)
    sd = {}
    for p, d in zip(zip(ci.tolist(), cj.tolist()), cd.tolist()):
        sd[p] = min(sd.get(p, np.inf), d)
    bd = dict(zip(zip(I.tolist(), J.tolist()), dmin.tolist()))
    brute_contacts = {p for p, d in bd.items() if d < b}
    sieve_contacts = {p for p, d in sd.items() if d < b}
    missed = brute_contacts - sieve_contacts
    # distance accuracy: local fine grid (dt=1e-4) recheck for near-threshold pairs
    near = [q for q in range(I.size) if dmin[q] < 3 * b]
    relf = []
    for q in near:
        i, j = int(I[q]), int(J[q])
        tg = np.linspace(max(0.0, tmin[q] - 0.05), tmin[q] + 0.05, 1001)
        x1, y1, x2, y2 = pair_states(a, e, varpi, M0, nn, np.full(tg.size, i), np.full(tg.size, j), tg)
        dfine = float(np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2).min())
        if (i, j) in sd:
            relf.append(abs(sd[(i, j)] - dfine) / max(dfine, 1e-12))
    rel = relf
    print(json.dumps({
        "validate": {"n": n, "T_orbits": T_orbits, "b": b, "dt": dt,
                     "brute_contacts": len(brute_contacts),
                     "sieve_contacts": len(sieve_contacts),
                     "brute_missed_by_sieve": len(missed),
                     "dist_rel_err_median": float(np.median(rel)) if rel else None,
                     "dist_rel_err_max": float(np.max(rel)) if rel else None}}, indent=1))
    return len(missed) == 0 and (not rel or np.max(rel) < 0.1)

if __name__ == "__main__":
    if "--validate" in sys.argv:
        ok = validate()
        print("VALIDATION", "PASS" if ok else "FAIL")
        sys.exit(0)
    bs = [1e-3, 1e-2]
    out = []
    for name, n, seed, To in [("TRAIN", 512, 11, 100), ("RING", 512, 12, 100),
                              ("RING_TIGHT", 512, 16, 100),
                              ("RING_MILD", 512, 13, 100), ("RING_BUNCH", 512, 14, 100),
                              ("BELT", 256, 15, 20)]:
        run_scene(name, n, seed, To, bs, out)
    with open("results.json", "w") as f:
        json.dump(out, f, indent=1)
    print("WROTE results.json")
