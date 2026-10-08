#!/usr/bin/env python3
"""Inversion probe: does 'every real encounter lies within partner rank 4 along the orbit'
(gold 20261006-0346-taleb-09b5) survive scenes the gold did not test — a fleet plus
different-n populations (eccentric crossers, a belt)?  2D plane, one star, Keplerian truth
aligned with crates/encounters/src/truth.rs: every pair-local minimum of distance below rho.

Certificate under test (operational semantics, disclosed in predictions.md): at refresh times
(cadence C per orbit) bodies are ordered by longitude lambda; an encounter is caught iff
fewer than k other bodies lie inside the shorter open arc between the partners at the LAST
refresh before its distance minimum (rank is the circular-ordering rank; k=4 is the claim).
  fleet-scope: ordering holds fleet members only (the natural 'sort the fleet' reading);
  global-scope: ordering holds all bodies.
"""
import json, sys, time
import numpy as np

GM = 4.0 * np.pi * np.pi   # AU^3 / yr^2
RHO = 1.5e-3               # encounter distance [AU]
T = 2.0                    # window [yr] = 2 orbits at 1 AU
COARSE = 129               # coarse samples over T
FLAG = 0.35                # coarse flag [AU]; > v_rel_max*dt_coarse ~ 0.24
REF_LEVELS, REF_SAMPLES = 3, 17

def kepler_xy_lam(a, e, w, M0, ts):
    """ts: (nt,). Returns positions (..., nt, 2) and longitudes (..., nt), broadcasting a/e/w/M0."""
    a, e, w, M0 = np.atleast_1d(a), np.atleast_1d(e), np.atleast_1d(w), np.atleast_1d(M0)
    shp = np.broadcast_shapes(a.shape, e.shape, w.shape, M0.shape)  # (nb,)
    n = np.sqrt(GM / a**3)
    M = (M0[..., None] + n[..., None] * ts) % (2 * np.pi)           # (nb, nt)
    E = M.copy()
    for _ in range(40):
        d = (E - e[..., None] * np.sin(E) - M) / (1.0 - e[..., None] * np.cos(E))
        E -= d
        if np.abs(d).max() < 1e-13:
            break
    cE, sE = np.cos(E), np.sin(E)
    xo = a[..., None] * (cE - e[..., None])
    yo = a[..., None] * np.sqrt(1 - e[..., None] ** 2) * sE
    cw, sw = np.cos(w)[..., None], np.sin(w)[..., None]
    x = xo * cw - yo * sw
    y = xo * sw + yo * cw
    nu = np.arctan2(np.sqrt(1 - e[..., None] ** 2) * sE, cE - e[..., None])
    lam = (w[..., None] + nu) % (2 * np.pi)
    return np.stack([x, y], -1), lam

def make_case(name, seed):
    r = np.random.default_rng(seed)
    def fleet(nf, spread):
        return (1.0 + spread * r.standard_normal(nf), np.zeros(nf),
                r.uniform(0, 2*np.pi, nf), r.uniform(0, 2*np.pi, nf), np.zeros(nf, int))
    if name == "fleet":
        return fleet(800, 1e-4)
    if name == "loose-fleet":
        return fleet(800, 1e-2)
    if name == "fleet+crossers":
        a1, e1, w1, m1, p1 = fleet(800, 1e-4)
        nx = 80
        q, Q = 1.0 - r.uniform(0.05, 0.5, nx), 1.0 + r.uniform(0.05, 0.5, nx)
        return (np.concatenate([a1, (q+Q)/2]), np.concatenate([e1, (Q-q)/(Q+q)]),
                np.concatenate([w1, r.uniform(0, 2*np.pi, nx)]),
                np.concatenate([m1, r.uniform(0, 2*np.pi, nx)]),
                np.concatenate([p1, np.ones(nx, int)]))
    if name == "fleet+belt":
        a1, e1, w1, m1, p1 = fleet(800, 1e-4)
        nb = 400
        return (np.concatenate([a1, r.uniform(0.9, 1.1, nb)]),
                np.concatenate([e1, r.uniform(0.0, 0.2, nb)]),
                np.concatenate([w1, r.uniform(0, 2*np.pi, nb)]),
                np.concatenate([m1, r.uniform(0, 2*np.pi, nb)]),
                np.concatenate([p1, np.ones(nb, int)]))
    raise ValueError(name)

def flagged_pairs(pos):
    nb = pos.shape[0]
    I, J = [], []
    for i in range(nb - 1):
        d = pos[i+1:] - pos[i]
        dm = np.einsum('ntk,ntk->nt', d, d).min(1)
        js = np.nonzero(dm < FLAG**2)[0] + i + 1
        I.append(np.full(len(js), i)); J.append(js)
    return np.concatenate(I), np.concatenate(J)

def refine_pair_min(a, e, w, M0, I, J, chunk=8000):
    """Bracketed coarse-to-fine minimum distance and its time for pairs (I,J)."""
    dt = T / (COARSE - 1)
    ts_c = np.linspace(0, T, COARSE)
    dmin = np.empty(len(I)); tmin = np.empty(len(I))
    grid = np.arange(REF_SAMPLES + 1)
    for lo in range(0, len(I), chunk):
        sl = slice(lo, min(lo+chunk, len(I)))
        ai, ei, wi, mi = a[I[sl]], e[I[sl]], w[I[sl]], M0[I[sl]]
        aj, ej, wj, mj = a[J[sl]], e[J[sl]], w[J[sl]], M0[J[sl]]
        pi = kepler_xy_lam(ai, ei, wi, mi, ts_c)[0]
        pj = kepler_xy_lam(aj, ej, wj, mj, ts_c)[0]
        d = np.sqrt(((pi - pj)**2).sum(-1))
        kb = d.argmin(1)
        tc = ts_c[kb]
        t_lo, t_hi = tc - dt, tc + dt
        dm = d[np.arange(len(kb)), kb]
        for _ in range(REF_LEVELS):
            span = (t_hi - t_lo) / REF_SAMPLES
            cand = t_lo[:, None] + span[:, None] * grid[None, :]
            pi = kepler_xy_lam(ai, ei, wi, mi, cand)[0]
            pj = kepler_xy_lam(aj, ej, wj, mj, cand)[0]
            dd = np.sqrt(((pi - pj)**2).sum(-1))
            kb = dd.argmin(1)
            dm = dd[np.arange(len(kb)), kb]
            tc = cand[np.arange(len(kb)), kb]
            t_lo, t_hi = tc - span, tc + span
        dmin[sl], tmin[sl] = dm, tc
    return dmin, tmin

def cert_ranks(lam_r, ii, jj):
    """Circular-ordering rank: bodies strictly inside the shorter open arc between partners."""
    nb = lam_r.size
    ranks = np.empty(len(ii), int)
    for m in range(len(ii)):
        li, lj = lam_r[ii[m]], lam_r[jj[m]]
        u = (lam_r - li) % (2 * np.pi)
        dl = (lj - li) % (2 * np.pi)
        if dl <= np.pi:
            ranks[m] = np.count_nonzero((u > 0) & (u < dl))
        else:
            ranks[m] = np.count_nonzero(u > dl)  # complement arc (dl, 2π), u==0 is i itself
    return ranks

def run_case(name, seed, cadences=(8, 16, 32, 64)):
    t0 = time.time()
    a, e, w, M0, pop = make_case(name, seed)
    nb = len(a)
    ts_c = np.linspace(0, T, COARSE)
    pos, _ = kepler_xy_lam(a, e, w, M0, ts_c)
    I, J = flagged_pairs(pos)
    dmin, tmin = refine_pair_min(a, e, w, M0, I, J)
    keep = dmin < RHO
    I, J, tmin = I[keep], J[keep], tmin[keep]
    ptype = np.where(pop[I] == pop[J], "intra", "cross")
    out = dict(name=name, seed=seed, nb=nb, flagged=len(dmin),
               E_intra=int((ptype == "intra").sum()), E_cross=int((ptype == "cross").sum()),
               cadences={})
    for C in cadences:
        tr = np.linspace(0, T, int(T * C), endpoint=False)
        _, lam = kepler_xy_lam(a, e, w, M0, tr)          # (nb, nrefresh)
        ridx = np.clip(np.searchsorted(tr, tmin, 'right') - 1, 0, len(tr) - 1)
        res = {}
        for scope in ("global", "fleet"):
            ranks = np.full(len(I), 10**9)
            for r in np.unique(ridx):
                m = ridx == r
                midx = np.nonzero(m)[0]
                ii, jj = I[m], J[m]
                if scope == "global":
                    ranks[m] = cert_ranks(lam[:, r], ii, jj)
                else:
                    sub = np.nonzero((pop[ii] == 0) & (pop[jj] == 0))[0]
                    if len(sub):
                        fl = np.nonzero(pop == 0)[0]
                        remap = -np.ones(nb, int); remap[fl] = np.arange(len(fl))
                        ranks[midx[sub]] = cert_ranks(lam[fl, r], remap[ii[sub]], remap[jj[sub]])
            for pt in ("intra", "cross"):
                mm = ptype == pt
                if not mm.any():
                    continue
                rr = ranks[mm]
                fin = rr[rr < 10**9]
                res[f"{scope}/{pt}"] = dict(
                    E=int(mm.sum()),
                    miss_k1=float((rr > 1).mean()), miss_k4=float((rr > 4).mean()),
                    miss_k8=float((rr > 8).mean()), miss_k16=float((rr > 16).mean()),
                    rank_p50=float(np.median(fin)) if len(fin) else None,
                    rank_p99=float(np.percentile(fin, 99)) if len(fin) else None,
                    rank_max=int(fin.max()) if len(fin) else None,
                    unreachable=float((rr >= 10**9).mean()))
        out["cadences"][C] = res
    out["wall_s"] = round(time.time() - t0, 1)
    return out

if __name__ == "__main__":
    name, seed = sys.argv[1], int(sys.argv[2])
    out = run_case(name, seed)
    with open(f"{name}-{seed}.json", "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "cadences"}))
    for C, res in out["cadences"].items():
        print(f"cadence {C}/orbit:", json.dumps(res))
