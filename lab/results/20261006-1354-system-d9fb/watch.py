#!/usr/bin/env python3
"""Storeless encounter watch vs the materialized tier. python3 watch.py [scene ...]
Scenes: uniform:N:seed highe:N clumped:N phalanx:N resonant:N  (rho=1e-4, T=20 orbits)"""
import numpy as np, json, sys, time

RHO = 1e-4
T = 20.0 * 2 * np.pi
TWOPI = 2 * np.pi
NEWT = 6

def rng(seed): return np.random.default_rng(seed)

def scene(name, N, seed):
    r = rng(seed)
    if name == "uniform":
        a = r.uniform(0.9, 1.1, N); e = np.abs(r.normal(0, 0.01, N))
    elif name == "highe":
        a = r.uniform(0.95, 1.05, N); e = r.uniform(0.7, 0.9, N)
    elif name == "clumped":
        a = r.uniform(0.9, 1.1, N); e = np.abs(r.normal(0, 0.05, N))
        k = N // 4; ci = r.choice(N, k, replace=False)
        a[ci] = 1.0 + r.uniform(-1e-5, 1e-5, k)
    elif name == "phalanx":
        nf = min(200, N // 3)
        a = np.concatenate([1.0 + r.uniform(-1e-5, 1e-5, nf), r.uniform(0.9, 1.1, N - nf)])
        e = np.concatenate([np.abs(r.normal(0, 0.001, nf)), np.abs(r.normal(0, 0.05, N - nf))])
        vp = np.concatenate([r.uniform(-0.1, 0.1, nf), r.uniform(0, TWOPI, N - nf)])
        l0 = np.concatenate([r.normal(0, 0.0628, nf) % TWOPI, r.uniform(0, TWOPI, N - nf)])
        return a, np.clip(e, 0, 0.95), vp, l0
    elif name == "resonant":
        bases = np.array([1.0, 2 ** (2 / 3), (3 / 2) ** (2 / 3)])
        ring = r.integers(0, 3, N)
        a = bases[ring] + r.normal(0, 1e-3, N); e = np.abs(r.normal(0, 0.01, N))
    else:
        raise SystemExit("scene?")
    return a, np.clip(e, 0, 0.95), r.uniform(0, TWOPI, N), r.uniform(0, TWOPI, N)

def kepler_E(M, e):
    E = M.copy()
    for _ in range(NEWT):
        E -= (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E

def state(a, e, vp, l0, n, t):
    lam = l0 + n * t
    E = kepler_E((lam - vp) % TWOPI, e)
    s, c = np.sin(E), np.cos(E)
    nu = np.arctan2(np.sqrt(np.maximum(1 - e * e, 1e-12)) * s, c - e)
    r = a * (1 - e * c)
    Lam = vp + nu
    return r * np.cos(Lam), r * np.sin(Lam), Lam

def C_e(e):
    """exact max |Lam-lam| (equation of center) per body: a table in e alone."""
    M = np.linspace(0, TWOPI, 2049)
    E = kepler_E(M, e)
    nu = np.arctan2(np.sqrt(np.maximum(1 - e * e, 1e-12)) * np.sin(E), np.cos(E) - e)
    return np.max(np.abs((nu - M + np.pi) % TWOPI - np.pi)) * 1.002 + 1e-12

# ---------------- method: storeless watch ----------------
def watch(a, e, vp, l0, n, Ce, want_roots=False, chunk=20000):
    N = len(a); rmin = a * (1 - e); rmax = a * (1 + e)
    ii, jj = np.triu_indices(N, 1); P = len(ii)
    pp_evals = np.zeros(P, np.int64); pp_epochs = np.zeros(P, np.int64)
    hits = []; roots_out = {}
    GBINS = [16, 32, 64, 128, 248]
    for s0 in range(0, P, chunk):
        s1 = min(s0 + chunk, P)
        i, j = ii[s0:s1], jj[s0:s1]
        pidx = np.arange(s0, s1)
        ok = (rmax[i] >= rmin[j] - 3 * RHO) & (rmax[j] >= rmin[i] - 3 * RHO)
        i, j, pidx = i[ok], j[ok], pidx[ok]
        if len(i) == 0: continue
        ai, aj, ei, ej = a[i], a[j], e[i], e[j]
        ni, nj = n[i], n[j]
        vpi, vpj, l0i, l0j = vp[i], vp[j], l0[i], l0[j]
        dlam0 = (l0[i] - l0[j] + np.pi) % TWOPI - np.pi
        W = Ce[i] + Ce[j]
        dn = ni - nj
        slow = np.abs(dn) < 1e-9
        # epochs per pair: intervals where |wrap(dlam0+dn t)| <= W
        # for dn!=0: t in [(-W+2pk-d0)/dn, (W+2pk-d0)/dn]; build ragged via slot loop
        maxslots = 80
        ev_pairs = np.zeros(len(i), np.int64); ep_pairs = np.zeros(len(i), np.int64)
        # gather all (pair-slot) intervals
        iv_lo = []; iv_hi = []; iv_pair = []
        for u in range(len(i)):
            if slow[u]:
                if abs(dlam0[u]) <= W[u]:
                    iv_lo.append(0.0); iv_hi.append(T); iv_pair.append(u)
                continue
            span = dn[u] * T
            kcen = (dlam0[u] + span / 2) / TWOPI
            klo = int(np.floor(kcen - (np.abs(span) / TWOPI + W[u] / np.pi) / 2) - 2)
            khi = int(np.ceil(kcen + (np.abs(span) / TWOPI + W[u] / np.pi) / 2) + 2)
            khi = min(khi, klo + maxslots)
            d0, Wd, dnu = dlam0[u], W[u], dn[u]
            kk = np.arange(klo, khi + 1)
            tA = (-Wd + TWOPI * kk - d0) / dnu
            tB = (+Wd + TWOPI * kk - d0) / dnu
            lo = np.clip(np.minimum(tA, tB), 0, T); hi = np.clip(np.maximum(tA, tB), 0, T)
            m = hi > lo
            if m.any():
                iv_lo.extend(lo[m].tolist()); iv_hi.extend(hi[m].tolist())
                iv_pair.extend([u] * int(m.sum()))
        if not iv_pair: continue
        iv_lo = np.array(iv_lo, float); iv_hi = np.array(iv_hi, float)
        iv_pair = np.array(iv_pair, np.int64)
        ep_pairs += np.bincount(iv_pair, minlength=len(i)).astype(np.int64)
        # grid size per interval: ~2.5 points/orbit, cap 104 (max epoch = T = 20 orbits)
        nbar = np.minimum(ni[iv_pair], nj[iv_pair])
        norb = (iv_hi - iv_lo) * nbar / TWOPI
        gneed = np.ceil(norb * 12 + 4).astype(int)
        for G in GBINS:
            prev = GBINS[GBINS.index(G) - 1] if GBINS.index(G) > 0 else 0
            sel = np.where((gneed > prev) & (gneed <= G))[0]
            if len(sel) == 0: continue
            tg = iv_lo[sel][:, None] + (iv_hi[sel] - iv_lo[sel])[:, None] * (
                np.arange(G)[None, :] / max(G - 1, 1))
            up = iv_pair[sel]
            IA = i[up]; JA = j[up]
            Ai = ai[up]; Ei_ = ei[up]; Vi = vpi[up]; Li_ = l0i[up]; Ni = ni[up]
            Aj = aj[up]; Ej = ej[up]; Vj = vpj[up]; Lj_ = l0j[up]; Nj = nj[up]
            def _register(u_arr, t_arr):
                nonlocal ev_pairs
                xi, yi, _ = state(a[i[u_arr]], e[i[u_arr]], vp[i[u_arr]], l0[i[u_arr]], n[i[u_arr]], t_arr)
                xj, yj, _ = state(a[j[u_arr]], e[j[u_arr]], vp[j[u_arr]], l0[j[u_arr]], n[j[u_arr]], t_arr)
                d2 = (xi - xj) ** 2 + (yi - yj) ** 2
                ev_pairs += np.bincount(u_arr, minlength=len(i)).astype(np.int64) * 2
                for WL, NP in ((0.15, 49), (0.015, 33)):
                    nu_ = np.where(d2 < (3.5 * RHO) ** 2)[0]
                    if len(nu_) == 0: break
                    ts = t_arr[nu_][:, None] + np.linspace(-WL, WL, NP)[None, :]
                    R_ = lambda q: np.repeat(q[nu_], NP)
                    x2, y2, _ = state(R_(a[i[u_arr]]), R_(e[i[u_arr]]), R_(vp[i[u_arr]]), R_(l0[i[u_arr]]), R_(n[i[u_arr]]), ts.ravel())
                    x3, y3, _ = state(R_(a[j[u_arr]]), R_(e[j[u_arr]]), R_(vp[j[u_arr]]), R_(l0[j[u_arr]]), R_(n[j[u_arr]]), ts.ravel())
                    d2r = (x2 - x3) ** 2 + (y2 - y3) ** 2
                    d2[nu_] = np.minimum(d2[nu_], np.minimum.reduceat(d2r, np.arange(len(nu_)) * NP))
                    ev_pairs += np.bincount(u_arr[nu_], minlength=len(i)).astype(np.int64) * (2 * NP)
                hm = d2 < RHO ** 2
                for uu in np.unique(u_arr[hm]):
                    m2 = hm & (u_arr == uu)
                    k = int(np.argmin(np.where(m2, d2, np.inf)))
                    hits.append((int(i[uu]), int(j[uu]), float(np.sqrt(d2[k]))))
                    if want_roots: roots_out.setdefault((int(i[uu]), int(j[uu])), []).append(float(t_arr[k]))
            # g on grid
            tgf = tg.ravel()
            _, _, Lia = state(np.repeat(Ai, G), np.repeat(Ei_, G), np.repeat(Vi, G), np.repeat(Li_, G), np.repeat(Ni, G), tgf)
            _, _, Lja = state(np.repeat(Aj, G), np.repeat(Ej, G), np.repeat(Vj, G), np.repeat(Lj_, G), np.repeat(Nj, G), tgf)
            ga = ((Lia - Lja + np.pi) % TWOPI - np.pi).reshape(len(sel), G)
            ev_pairs += np.bincount(np.repeat(up, G), minlength=len(i)).astype(np.int64) * 2
            # brackets from sign changes
            sc = ga[:, :-1] * ga[:, 1:] < 0
            bi, bjj = np.where(sc)
            if len(bi):
                blo = tg[bi, bjj]; bhi = tg[bi, bjj + 1]; bu = up[bi]
                for _ in range(26):
                    mid = 0.5 * (blo + bhi)
                    _, _, lm = state(IA[bi], e[IA[bi]], vp[IA[bi]], l0[IA[bi]], n[IA[bi]], mid)
                    _, _, ln = state(JA[bi], e[JA[bi]], vp[JA[bi]], l0[JA[bi]], n[JA[bi]], mid)
                    gm = (lm - ln + np.pi) % TWOPI - np.pi
                    go = (ga[bi, bjj] >= 0) == (gm >= 0)
                    blo = np.where(go, mid, blo); bhi = np.where(go, bhi, mid)
                    ev_pairs += np.bincount(bu, minlength=len(i)).astype(np.int64) * 2
                roots_t = 0.5 * (blo + bhi)
                rt_u = bu
                _register(rt_u, roots_t)
            # tangency: local |g| minima below 1e-3 -> golden refine
            gabs = np.abs(ga)
            tmin = (gabs[:, 1:-1] < gabs[:, :-2]) & (gabs[:, 1:-1] < gabs[:, 2:]) & (gabs[:, 1:-1] < 1e-3)
            ti, tj = np.where(tmin)
            if len(ti):
                tlo = np.maximum(tg[ti, tj], tg[ti, tj] - 0.0); tlo = tg[ti, tj] - 0.25 * (tg[ti, tj + 1] - tg[ti, tj - 1])
                thi = tg[ti, tj] + 0.25 * (tg[ti, tj + 1] - tg[ti, tj - 1])
                tu = up[ti]
                for _ in range(30):
                    m1 = tlo + 0.382 * (thi - tlo); m2 = tlo + 0.618 * (thi - tlo)
                    _, _, l1 = state(IA[ti], e[IA[ti]], vp[IA[ti]], l0[IA[ti]], n[IA[ti]], m1)
                    _, _, l2 = state(JA[ti], e[JA[ti]], vp[JA[ti]], l0[JA[ti]], n[JA[ti]], m1)
                    f1 = np.abs((l1 - l2 + np.pi) % TWOPI - np.pi)
                    _, _, l1 = state(IA[ti], e[IA[ti]], vp[IA[ti]], l0[IA[ti]], n[IA[ti]], m2)
                    _, _, l2 = state(JA[ti], e[JA[ti]], vp[JA[ti]], l0[JA[ti]], n[JA[ti]], m2)
                    f2 = np.abs((l1 - l2 + np.pi) % TWOPI - np.pi)
                    go2 = f1 <= f2
                    thi = np.where(go2, m2, thi); tlo = np.where(go2, tlo, m1)
                    ev_pairs += np.bincount(tu, minlength=len(i)).astype(np.int64) * 4
                roots_t2 = 0.5 * (tlo + thi); rt2_u = tu
                _register(rt2_u, roots_t2)
        # per-epoch golden-section minimum of d^2 (tangency dips the grid misses)
        for G in GBINS:
            prev = GBINS[GBINS.index(G) - 1] if GBINS.index(G) > 0 else 0
            sel2 = np.where((gneed > prev) & (gneed <= G))[0]
            if len(sel2) == 0: continue
            glo = iv_lo[sel2]; ghi = iv_hi[sel2]; gu = iv_pair[sel2]
            ga_ = glo.copy(); gb_ = ghi.copy()
            for _ in range(42):
                m1 = ga_ + 0.382 * (gb_ - ga_); m2 = ga_ + 0.618 * (bb := gb_ - ga_)
                x1, y1, _ = state(a[i[gu]], e[i[gu]], vp[i[gu]], l0[i[gu]], n[i[gu]], m1)
                x2, y2, _ = state(a[j[gu]], e[j[gu]], vp[j[gu]], l0[j[gu]], n[j[gu]], m1)
                f1 = (x1 - x2) ** 2 + (y1 - y2) ** 2
                x1, y1, _ = state(a[i[gu]], e[i[gu]], vp[i[gu]], l0[i[gu]], n[i[gu]], m2)
                x2, y2, _ = state(a[j[gu]], e[j[gu]], vp[j[gu]], l0[j[gu]], n[j[gu]], m2)
                f2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
                take1 = f1 <= f2
                gb_ = np.where(take1, m2, gb_); ga_ = np.where(take1, ga_, m1)
                ev_pairs += np.bincount(gu, minlength=len(i)).astype(np.int64) * 4
            tgold = 0.5 * (ga_ + gb_)
            # register with wide refine (dips can sit far from any alignment root)
            xi, yi, _ = state(a[i[gu]], e[i[gu]], vp[i[gu]], l0[i[gu]], n[i[gu]], tgold)
            xj, yj, _ = state(a[j[gu]], e[j[gu]], vp[j[gu]], l0[j[gu]], n[j[gu]], tgold)
            d2g = (xi - xj) ** 2 + (yi - yj) ** 2
            ev_pairs += np.bincount(gu, minlength=len(i)).astype(np.int64) * 2
            nu_ = np.where(d2g < (3.5 * RHO) ** 2)[0]
            if len(nu_):
                ts = tgold[nu_][:, None] + np.linspace(-0.3, 0.3, 65)[None, :]
                R_ = lambda q: np.repeat(q[nu_], 65)
                x2, y2, _ = state(R_(a[i[gu]]), R_(e[i[gu]]), R_(vp[i[gu]]), R_(l0[i[gu]]), R_(n[i[gu]]), ts.ravel())
                x3, y3, _ = state(R_(a[j[gu]]), R_(e[j[gu]]), R_(vp[j[gu]]), R_(l0[j[gu]]), R_(n[j[gu]]), ts.ravel())
                d2r = (x2 - x3) ** 2 + (y2 - y3) ** 2
                d2g[nu_] = np.minimum(d2g[nu_], np.minimum.reduceat(d2r, np.arange(len(nu_)) * 65))
                ev_pairs += np.bincount(gu[nu_], minlength=len(i)).astype(np.int64) * 130
                hm = d2g < RHO ** 2
                for uu in np.unique(gu[hm]):
                    hits.append((int(i[uu]), int(j[uu]), float(np.sqrt(np.min(d2g[gu == uu])))))
        pp_evals[pidx] = ev_pairs
        pp_epochs[pidx] = ep_pairs
    return dict(hits=hits, evals=int(pp_evals.sum()), pp_evals=pp_evals,
                pp_epochs=pp_epochs, roots=roots_out)

# ---------------- truth: theorem-filtered dense + anomaly audit ----------------
def _mind(a, e, vp, l0, n, I, J, ts):
    xi, yi, _ = state(a[I], e[I], vp[I], l0[I], n[I], ts)
    xj, yj, _ = state(a[J], e[J], vp[J], l0[J], n[J], ts)
    d2 = (xi - xj) ** 2 + (yi - yj) ** 2
    k = int(np.argmin(d2))
    return float(d2[k]), float(ts[k])

def truth(a, e, vp, l0, n, samples_per_orbit=None, audit_frac=0.02, seed=0):
    if samples_per_orbit is None:
        samples_per_orbit = 64 if len(a) <= 500 else 40
    N = len(a); rmin = a * (1 - e); rmax = a * (1 + e)
    ii, jj = np.triu_indices(N, 1)
    r = rng(seed); audit_mask = r.random(len(ii)) < audit_frac
    enc = []
    for s0 in range(0, len(ii), 4000):
        i, j = ii[s0:s0 + 4000], jj[s0:s0 + 4000]
        am = audit_mask[s0:s0 + 4000]
        ok = ((rmax[i] >= rmin[j] - 4 * RHO) & (rmax[j] >= rmin[i] - 4 * RHO)) | am
        for u in np.where(ok)[0]:
            I, J = int(i[u]), int(j[u])
            nbar = min(n[I], n[J])
            ns = int(np.clip(T * nbar / TWOPI * samples_per_orbit, 64, 40000))
            ts = np.linspace(0, T, ns)
            d2m, tstar = _mind(a, e, vp, l0, n, I, J, ts)
            vrel = max(abs(n[I] - n[J]), 2 * (e[I] + e[J]) * nbar) * max(a[I], a[J])
            step = ts[1] - ts[0]
            if d2m < (vrel * step * 1.5 + 8 * RHO) ** 2:
                ts2 = np.linspace(max(0, tstar - 3 * step), min(T, tstar + 3 * step), 1500)
                d2m, tstar = _mind(a, e, vp, l0, n, I, J, ts2)
            if d2m < RHO ** 2:
                enc.append((I, J, float(np.sqrt(d2m)), tstar, bool(am[u])))
    return enc

def adjudicate(a, e, vp, l0, n, I, J, t0):
    nbar = min(n[I], n[J])
    ts = np.linspace(max(0, t0 - 0.6 * TWOPI / nbar), min(T, t0 + 0.6 * TWOPI / nbar), 8000)
    d2, tstar = _mind(a, e, vp, l0, n, I, J, ts)
    ts2 = np.linspace(max(0, tstar - 0.02 * TWOPI / nbar), min(T, tstar + 0.02 * TWOPI / nbar), 3000)
    d2, _ = _mind(a, e, vp, l0, n, I, J, ts2)
    return float(np.sqrt(d2))

def main():
    specs = sys.argv[1:] or ["uniform:250:1", "uniform:500:1", "uniform:1000:1",
                             "highe:400:2", "clumped:800:3", "phalanx:800:4", "resonant:600:5"]
    out = {}
    for spec in specs:
        nm, Ns, sd = spec.split(":"); N, sd = int(Ns), int(sd)
        a, e, vp, l0 = scene(nm, N, sd); n = a ** -1.5
        Ce = np.array([C_e(x) for x in e])
        t0 = time.time(); meth = watch(a, e, vp, l0, n, Ce, want_roots=True); wt = time.time() - t0
        t0 = time.time(); tr = truth(a, e, vp, l0, n); tt = time.time() - t0
        mset = {(i, j): d for i, j, d in meth["hits"]}
        tset = {(I, J): (d, ts) for I, J, d, ts, _ in tr}
        problems = []
        for k in tset:
            if k not in mset:
                d, ts = tset[k]
                dd = adjudicate(a, e, vp, l0, n, k[0], k[1], ts)
                if dd < RHO: problems.append([list(k), round(dd, 7), "REAL miss"])
                else: pass  # truth false positive from coarse grid
        for k in mset:
            if k not in tset:
                ts = meth["roots"].get(k, [T / 2])[0]
                dd = adjudicate(a, e, vp, l0, n, k[0], k[1], ts)
                if dd < RHO: problems.append([list(k), round(dd, 7), "method-only confirmed (truth grid missed)"])
                else: problems.append([list(k), round(dd, 7), "FALSE ALARM"])
        cl = 0; cl_caught = 0
        for (I, J) in tset:
            dn = n[I] - n[J]
            dl = (l0[I] - l0[J] + np.pi) % TWOPI - np.pi
            conj = (abs(dn) >= 1e-12) and any(0 <= (-dl + TWOPI * k) / dn <= T for k in range(-40, 41))
            if not conj:
                cl += 1
                if (I, J) in mset: cl_caught += 1
        rmin, rmax = a * (1 - e), a * (1 + e)
        ii, jj = np.triu_indices(N, 1)
        cone = int(np.sum((rmax[ii] >= rmin[jj] - RHO) & (rmax[jj] >= rmin[ii] - RHO)))
        res = dict(scene=spec, N=N, watch_s=round(wt, 1), truth_s=round(tt, 1),
                   enc_truth=len(tset), enc_method=len(mset), problems=problems[:10],
                   n_problems=len(problems), conjunctionless=cl, cl_caught_by_watch=cl_caught,
                   watch_evals=meth["evals"],
                   evals_per_enc=round(meth["evals"] / max(len(tset), 1), 1),
                   epochs=int(meth["pp_epochs"].sum()),
                   pp_evals_max=int(meth["pp_evals"].max()),
                   pp_epochs_max=int(meth["pp_epochs"].max()),
                   cone_pairs=cone, certs=2 * N,
                   cone_frac=round(cone / (N * (N - 1) / 2), 4))
        out[spec] = res; print(json.dumps(res), flush=True)
    with open(__file__.replace("watch.py", "metrics.json"), "w") as f:
        json.dump(out, f, indent=1)

if __name__ == "__main__":
    main()
