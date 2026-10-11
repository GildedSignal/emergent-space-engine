#!/usr/bin/env python3
"""Inversion probe: does the static phase-neighbour (rank-k) certificate find
the real encounters of a QUIET co-orbital concentration (no kicks, the design's
steady state)?

Truth: exact Kepler motion about one dominant mass (GM=1, a0=1, P0=2*pi).
Close approaches of a co-orbital pair happen only at conjunctions in true
longitude (d_lambda = 0 mod 2pi); we find every such crossing on a grid,
bisect it to ~1e-3 rad in longitude, and take the exact 2-D distance there.
Dips away from a longitude conjunction cannot be close for b << r (the
tangential term r*|d_lambda| dominates); the brute-force control measures any
residual miss.

Scenes: A ring, B fleet, C1 lockstep, C2 brute control, S smoke.
Usage: python3 probe.py <scene> [seed]  -> <scene>-s<seed>.json + encounters csv.gz
Rank convention everywhere: rank[i->j] = number of OTHER bodies strictly closer
to i than j (in the given circular coordinate). Catch_k = rank <= k, i.e. j is
among i's (k+1) nearest.
"""
import gzip
import json
import sys
import time

import numpy as np

TWO_PI = 2.0 * np.pi
P0 = TWO_PI  # a0=1, GM=1


def wrap(x):
    return (x + np.pi) % TWO_PI - np.pi


def keplerE(M, e, iters=12):
    E = M.copy()
    for _ in range(iters):
        E = E - (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    return E


def lam_r(M, e, w, a):
    """True longitude and radius at mean anomaly M."""
    E = keplerE(M, e)
    nu = 2.0 * np.arctan2(np.sqrt(1.0 + e) * np.sin(E / 2.0),
                          np.sqrt(1.0 - e) * np.cos(E / 2.0))
    r = a * (1.0 - e * np.cos(E))
    return w + nu, r


SCENES = {
    "A":  dict(N=600, sa=3e-3, e0=0.05, se=3e-3, sw=3e-3, cluster=None, T=128 * P0, S=2048),
    "B":  dict(N=600, sa=3e-4, e0=0.10, se=1e-3, sw=1e-3, cluster=0.05, T=128 * P0, S=2048),
    "C1": dict(N=600, sa=1e-6, e0=0.10, se=1e-4, sw=1e-4, cluster=0.05, T=16 * P0, S=1024),
    "S":  dict(N=60,  sa=3e-3, e0=0.05, se=3e-3, sw=3e-3, cluster=None, T=8 * P0, S=1024),

    "S2": dict(N=60, sa=3e-4, e0=0.10, se=1e-3, sw=1e-3, cluster=0.05, T=8 * P0, S=1024),
}


def make_bodies(sc, rng):
    N = sc["N"]
    a = 1.0 + sc["sa"] * rng.standard_normal(N)
    e = np.clip(sc["e0"] + sc["se"] * rng.standard_normal(N), 1e-4, 0.4)
    w = sc["sw"] * rng.standard_normal(N)
    if sc["cluster"] is None:
        M0 = rng.uniform(0.0, TWO_PI, N)
    else:
        M0 = sc["cluster"] * rng.standard_normal(N)
    n = a ** -1.5
    return a, e, w, M0, n

def circular_ranks(coord):
    """rank[i,j] = #{k != i: |wrap(coord_k - coord_i)| < |wrap(coord_j - coord_i)|}."""
    N = len(coord)
    d = np.abs(wrap(coord[None, :] - coord[:, None]))
    order = np.argsort(d, axis=1, kind="stable")
    rank = np.empty((N, N), dtype=np.int32)
    rows = np.arange(N)[:, None]
    rank[rows, order] = np.arange(N, dtype=np.int32)[None, :]
    rank = np.maximum(rank - 1, 0)  # drop self from the count; self stays 0
    return rank


def rank_at_times(ev_i, ev_gap_src, eval_times, coord0, rates):
    """Per event: rank of partner j among i's circular neighbours in the
    coordinate x(t) = coord0 + rates*t, evaluated at time eval_times (per event).
    ev_gap_src: the partner's coordinate minus i's, at the same eval_times."""
    E = len(ev_i)
    N = len(coord0)
    out = np.empty(E, dtype=np.int32)
    chunk = max(1, int(4e6 // N))
    for s in range(0, E, chunk):
        t = eval_times[s:s + chunk][:, None]              # (c,1)
        X = coord0[None, :] + rates[None, :] * t          # (c,N)
        pi = ev_i[s:s + chunk]
        rows = np.arange(len(pi))
        xi = X[rows, pi][:, None]
        gap = np.abs(wrap(X - xi))
        pgap = np.abs(wrap(ev_gap_src[s:s + chunk]))
        cnt = (gap < pgap[:, None]).sum(axis=1)
        out[s:s + chunk] = np.maximum(cnt - 1, 0)  # self has gap 0
    return out



def find_conjunctions(a, e, w, M0, n, sc, verbose=True):
    """Every close-approach candidate in [0,T]: (pi, pj, tstar, lamstar_i, dist).

    Two detector classes, unioned and deduped:
    1. longitude-conjunction crossings (fast pairs: the dip sits at dl=0);
    2. grid local minima of the pair distance, refined by ternary search
       (slow/near-twin pairs: the dip is displaced from dl=0, or never crosses).
    Only dips whose grid distance < dip_cut are refined (deep dips cannot
    refine below b by more than the grid overshoot; the brute control bounds
    the residue)."""
    N = len(a)
    S, T = sc["S"], sc["T"]
    dip_cut = 10 * 3e-4  # refine grid dips below 10 * max b
    tgrid = np.linspace(0.0, T, S + 1)
    t0 = time.time()
    lamg = np.empty((N, S + 1)); rg = np.empty((N, S + 1))
    for i in range(N):
        lamg[i], rg[i] = lam_r(M0[i] + n[i] * tgrid, e[i], w[i], a[i])
    if verbose:
        print(f"  grid {N}x{S+1} kepler: {time.time()-t0:.1f}s", flush=True)

    ii, jj = np.triu_indices(N, k=1)
    P = len(ii)
    B = 6000
    parts = []  # (pi, pj, lo, hi, flo) crossing brackets
    dips = []   # (pi, pj, t_center) grid local minima below cut
    t0 = time.time()
    for s in range(0, P, B):
        bi, bj = ii[s:s + B], jj[s:s + B]
        li, ri = lamg[bi], rg[bi]
        lj, rj = lamg[bj], rg[bj]
        dl = wrap(lj - li)
        # class 1: crossings
        s0, s1 = dl[:, :-1], dl[:, 1:]
        m = (s0 * s1 <= 0.0) & (np.abs(s0) + np.abs(s1) < np.pi) \
            & (np.abs(s0) > 1e-13) & (np.abs(s1) > 1e-13)
        pb, kb = np.nonzero(m)
        parts.append((bi[pb], bj[pb], tgrid[kb], tgrid[kb + 1], s0[pb, kb]))
        # class 2: grid local minima of the distance
        d2 = ri*ri + rj*rj - 2.0*ri*rj*np.cos(li - lj)
        d = np.sqrt(np.maximum(d2, 0.0))
        dm = (d[:, 1:-1] <= d[:, :-2]) & (d[:, 1:-1] < d[:, 2:]) & (d[:, 1:-1] < dip_cut)
        db, kb = np.nonzero(dm)
        dips.append((bi[db], bj[db], tgrid[kb + 1], d[db, kb + 1]))
    cpi = np.concatenate([p[0] for p in parts]); cpj = np.concatenate([p[1] for p in parts])
    clo = np.concatenate([p[2] for p in parts]); chi = np.concatenate([p[3] for p in parts])
    cflo = np.concatenate([p[4] for p in parts])
    dpi = np.concatenate([d[0] for d in dips]); dpj = np.concatenate([d[1] for d in dips])
    dtc = np.concatenate([d[2] for d in dips]); ddc = np.concatenate([d[3] for d in dips])
    if verbose:
        print(f"  {len(cpi)} crossings + {len(dpi)} grid dips < {dip_cut}: {time.time()-t0:.1f}s", flush=True)

    def dist_at(pt, pi_, pj_):
        li, ri = lam_r(M0[pi_] + n[pi_] * pt, e[pi_], w[pi_], a[pi_])
        lj, rj = lam_r(M0[pj_] + n[pj_] * pt, e[pj_], w[pj_], a[pj_])
        dd = np.sqrt(np.maximum(ri*ri + rj*rj - 2.0*ri*rj*np.cos(li - lj), 0.0))
        return dd, li

    # refine class 1: bisect the dl crossing
    t0 = time.time()
    lo, hi, slo = clo.copy(), chi.copy(), cflo
    for _ in range(10):
        mid = 0.5 * (lo + hi)
        li_, ri_ = lam_r(M0[cpi] + n[cpi] * mid, e[cpi], w[cpi], a[cpi])
        lj_, rj_ = lam_r(M0[cpj] + n[cpj] * mid, e[cpj], w[cpj], a[cpj])
        fm = wrap(lj_ - li_)
        same = np.sign(fm) == np.sign(slo)
        lo = np.where(same, mid, lo)
        hi = np.where(same, hi, mid)
    t1c = 0.5 * (lo + hi)
    d1c, l1c = dist_at(t1c, cpi, cpj)
    if verbose:
        print(f"  bisect {len(t1c)} crossings: {time.time()-t0:.1f}s", flush=True)

    # refine class 2: ternary search on the distance around the grid dip
    t0 = time.time()
    if len(dpi):
        span = tgrid[1] - tgrid[0]
        tlo = np.maximum(dtc - span, 0.0); thi = np.minimum(dtc + span, T)
        for _ in range(24):
            m1 = tlo + (thi - tlo) / 3.0
            m2 = thi - (thi - tlo) / 3.0
            f1, _ = dist_at(m1, dpi, dpj)
            f2, _ = dist_at(m2, dpi, dpj)
            take_left = f1 < f2
            thi = np.where(take_left, m2, thi)
            tlo = np.where(take_left, tlo, m1)
        t2c = 0.5 * (tlo + thi)
        d2c, l2c = dist_at(t2c, dpi, dpj)
    else:
        t2c = np.empty(0); d2c = np.empty(0); l2c = np.empty(0)
    if verbose:
        print(f"  ternary {len(t2c)} dips: {time.time()-t0:.1f}s", flush=True)

    # union, dedupe by (pair, |dt| < P0/16)
    pi = np.concatenate([cpi, dpi]); pj = np.concatenate([cpj, dpj])
    tstar = np.concatenate([t1c, t2c]); dist = np.concatenate([d1c, d2c])
    lamstar = np.concatenate([l1c, l2c])
    if len(pi):
        key = pi.astype(np.int64) * N + pj
        order = np.lexsort((tstar, key))
        pi, pj, tstar, dist, lamstar, key = pi[order], pj[order], tstar[order], dist[order], lamstar[order], key[order]
        # cluster events of one pair closer than P0/16 in time; keep the MINIMUM
        # distance event of each cluster (a crossing and its adjacent dip are one
        # physical approach)
        new_run = np.empty(len(pi), dtype=bool)
        new_run[0] = True
        new_run[1:] = (key[1:] != key[:-1]) | (np.abs(tstar[1:] - tstar[:-1]) >= P0 / 16.0)
        run_id = np.cumsum(new_run)
        order2 = np.lexsort((dist, run_id))          # min dist first per run
        pi, pj, tstar, dist, lamstar, run_id = pi[order2], pj[order2], tstar[order2], dist[order2], lamstar[order2], run_id[order2]
        first = np.empty(len(pi), dtype=bool)
        first[0] = True
        first[1:] = run_id[1:] != run_id[:-1]
        pi, pj, tstar, dist, lamstar = pi[first], pj[first], tstar[first], dist[first], lamstar[first]
    if verbose:
        print(f"  truth events after dedupe: {len(pi)}", flush=True)
    return pi, pj, tstar, lamstar, dist, lamg[:, 0]



def analyse(scene_name, seed=0, verbose=True):
    sc = SCENES[scene_name]
    rng = np.random.default_rng(seed)
    a, e, w, M0, n = make_bodies(sc, rng)

    pi, pj, tstar, lamstar, dist, lam0 = find_conjunctions(a, e, w, M0, n, sc, verbose)
    N = len(a)
    C = len(pi)

    rankM = circular_ranks(M0)
    rankL = circular_ranks(lam0)
    rankn = circular_ranks(n)
    rM_ij = np.minimum(rankM[pi, pj], rankM[pj, pi]).astype(np.int64)
    rL_ij = np.minimum(rankL[pi, pj], rankL[pj, pi]).astype(np.int64)
    rn_ij = np.minimum(rankn[pi, pj], rankn[pj, pi]).astype(np.int64)

    # rank at the encounter instant (mean anomaly)
    gap_at = (M0[pj] + n[pj] * tstar) - (M0[pi] + n[pi] * tstar)
    rM_at = rank_at_times(pi, gap_at, tstar, M0, n)
    # rank at the last orbit boundary before the encounter (per-orbit cadence)
    t_eval = np.floor(tstar / P0) * P0
    gap_ev = (M0[pj] + n[pj] * t_eval) - (M0[pi] + n[pi] * t_eval)
    rM_ev = rank_at_times(pi, gap_ev, t_eval, M0, n)

    tri = np.triu_indices(N, 1)
    dn_pairs = np.abs(n[None, :] - n[:, None])[tri]
    dM = np.abs(wrap(M0[None, :] - M0[:, None]))
    np.fill_diagonal(dM, np.inf)
    g_nn = float(dM.min(axis=1).mean())   # mean nearest-neighbour circular gap
    out = dict(scene=scene_name, seed=seed, N=N, T_orbits=sc["T"] / P0, events=C,
               params={k: sc[k] for k in ("sa", "e0", "se", "sw", "cluster")},
               median_abs_dn=float(np.median(dn_pairs)),
               mean_nn_phase_gap=g_nn)
    out["Xi_rank4"] = out["median_abs_dn"] * sc["T"] / (4 * max(g_nn, 1e-15))

    for b in (1e-4, 3e-4):
        enc = dist < b
        E = int(enc.sum())
        res = dict(encounters=E, b=b)
        if E:
            rr = rM_ij[enc]
            res.update(
                catch_static_rank4_phaseM=float((rr <= 4).mean()),
                catch_static_rank4_phaseL=float((rL_ij[enc] <= 4).mean()),
                catch_static_rank4_n=float((rn_ij[enc] <= 4).mean()),
                catch_static_rank16_phaseM=float((rr <= 16).mean()),
                catch_pertorbit_rank4=float((rM_ev[enc] <= 4).mean()),
                catch_attime_rank4=float((rM_at[enc] <= 4).mean()),
                median_setup_rank=float(np.median(rr)),
                p90_setup_rank=float(np.percentile(rr, 90)),
                max_setup_rank=int(rr.max()),
                median_rank_attime=float(np.median(rM_at[enc])),
            )
        out[f"b={b}"] = res

    out["pairs_with_conjunction"] = int(len(np.unique(pi.astype(np.int64) * N + pj)))
    out["conjunctions_per_body_per_orbit"] = C / N / (sc["T"] / P0)

    enc_all = dist < 3e-4
    with gzip.open(f"{scene_name}-s{seed}-encounters.csv.gz", "wt") as f:
        f.write("i,j,t_orbits,lam,dist,rankM_setup,rankL_setup,rankn_setup,rankM_attime,rankM_pertorbit\n")
        for k in np.nonzero(enc_all)[0]:
            f.write(f"{pi[k]},{pj[k]},{tstar[k]/P0:.6f},{lamstar[k]:.6f},{dist[k]:.3e},"
                    f"{rM_ij[k]},{rL_ij[k]},{rn_ij[k]},{rM_at[k]},{rM_ev[k]}\n")
    return out


def brute_control():
    """Dense-sampling truth vs the event finder, on two small scenes:
    S (ring-like) and S2 (clustered fleet, encounter-rich)."""
    all_res = {}
    for name, seed in (("S", 7), ("S2", 11)):
        sc = dict(SCENES[name])
        rng = np.random.default_rng(seed)
        a, e, w, M0, n = make_bodies(sc, rng)
        N = len(a)
        T, Sb = sc["T"], 65536
        tgrid = np.linspace(0.0, T, Sb)
        lam = np.empty((N, Sb)); rr = np.empty((N, Sb))
        for i in range(N):
            lam[i], rr[i] = lam_r(M0[i] + n[i] * tgrid, e[i], w[i], a[i])
        ii, jj = np.triu_indices(N, k=1)
        P = len(ii)
        brute_min = np.full(P, np.inf)
        t0 = time.time()
        B = 300
        for s in range(0, P, B):
            li, ri = lam[ii[s:s+B]], rr[ii[s:s+B]]
            lj, rj = lam[jj[s:s+B]], rr[jj[s:s+B]]
            d2 = ri*ri + rj*rj - 2.0*ri*rj*np.cos(li - lj)
            brute_min[s:s+B] = np.sqrt(d2).min(axis=1)
        print(f"  [{name}] brute {P} pairs x {Sb}: {time.time()-t0:.1f}s", flush=True)

        pi, pj, tstar, lamstar, dist, lam0 = find_conjunctions(a, e, w, M0, n, sc, verbose=False)
        ev_min = np.full(P, np.inf)
        key = ii.astype(np.int64) * N + jj
        np.minimum.at(ev_min, np.searchsorted(key, pi.astype(np.int64) * N + pj), dist)

        res = dict(N=N, T_orbits=T / P0, seed=seed, events=len(pi))
        for b in (1e-4, 3e-4):
            tb, te = brute_min < b, ev_min < b
            res[f"b={b}"] = dict(
                brute_encounters=int(tb.sum()), event_encounters=int(te.sum()),
                brute_only=int((tb & ~te).sum()), event_only=int((te & ~tb).sum()),
                agree=int((tb & te).sum()))
        both = (brute_min < 3e-4) & (ev_min < 3e-4)
        res["max_rel_dev_below_3e-4"] = float(
            (np.abs(brute_min[both] - ev_min[both]) / brute_min[both]).max()) if both.any() else None
        rankM = circular_ranks(M0)
        rM_ij = np.minimum(rankM[ii, jj], rankM[jj, ii]).astype(np.int64)
        for b in (1e-4, 3e-4):
            tb = brute_min < b
            if tb.sum():
                res[f"b={b}"]["catch_static_rank4_phaseM_on_brute_truth"] = float((rM_ij[tb] <= 4).mean())
                res[f"b={b}"]["median_setup_rank_on_brute_truth"] = float(np.median(rM_ij[tb]))
        all_res[name] = res
    return all_res


if __name__ == "__main__":
    name = sys.argv[1]
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    out = brute_control() if name == "C2" else analyse(name, seed)
    print(json.dumps(out, indent=1))
    with open(f"{name}-s{seed}.json", "w") as f:
        json.dump(out, f, indent=1)
