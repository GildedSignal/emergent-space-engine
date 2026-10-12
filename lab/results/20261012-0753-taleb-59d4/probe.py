#!/usr/bin/env python3
"""Red-team probe for the train certificate (rank<=4) adopted from gold 20261006-0346-taleb-09b5.

Independent harness: numpy Kepler propagation, brute all-pairs distance minima on a common
time grid, vectorized ternary refinement of t*, ranks of the partner at closest approach in
three keys (3D distance = what the gold measured, true longitude = sound phase key,
mean longitude = the design's likely sort key). rho = 1e-4, a = 1, mu = 1.
"""
import json
import sys
import time
import numpy as np

TAU = 2.0 * np.pi
RHO = 1e-4
E_CAP = 0.01  # matches the gold's rayleigh(0.001, 0.01) cap


def make_fleet(nc, a_hw, sig_lam, sig_e, seed, pom_spread=0.1):
    rng = np.random.default_rng(seed)
    a = 1.0 + (2.0 * rng.random(nc) - 1.0) * a_hw
    e = np.minimum(sig_e * np.sqrt(-2.0 * np.log(1e-12 + rng.random(nc))),
                   max(E_CAP, 3 * sig_e))
    pom = TAU * rng.random() + (2.0 * rng.random(nc) - 1.0) * pom_spread
    lam0 = TAU * rng.random()
    lam = (lam0 + sig_lam * rng.standard_normal(nc)) if sig_lam > 0 else TAU * rng.random(nc)
    M0 = np.mod(lam - pom, TAU)
    return a, e, pom, M0


def kepler_E(e, M):
    E = M.copy()
    for _ in range(10):
        E = E - (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    return E


def states(a, e, pom, M0, t):
    """a,e,pom,M0: (N,); t: (T,) -> pos (N,T,2), true/mean longitude (N,T)."""
    M = np.mod(M0[:, None] + (a ** -1.5)[:, None] * t[None, :], TAU)
    E = kepler_E(e[:, None], M)
    r = a[:, None] * (1.0 - e[:, None] * np.cos(E))
    nu = 2.0 * np.arctan2(np.sqrt(1 + e)[:, None] * np.sin(E),
                          np.sqrt(1 - e)[:, None] * np.cos(E))
    lt = np.mod(pom[:, None] + nu, TAU)
    pos = np.stack([r * np.cos(lt), r * np.sin(lt)], -1)
    return pos, lt, np.mod(pom[:, None] + M, TAU)


def grid_min(a, e, pom, M0, T, dt):
    ts = np.arange(0.0, T, dt)
    N = a.size
    best_d = np.full((N, N), np.inf)
    best_t = np.zeros((N, N))
    for k in range(ts.size):
        xy = states(a, e, pom, M0, ts[k:k + 1])[0][:, 0, :]
        rx = xy[:, 0][:, None] - xy[:, 0][None, :]
        ry = xy[:, 1][:, None] - xy[:, 1][None, :]
        d = np.sqrt(rx * rx + ry * ry)
        upd = d < best_d
        best_d = np.where(upd, d, best_d)
        best_t = np.where(upd, ts[k], best_t)
    return best_d, best_t


def pair_dist(a, e, pom, M0, ii, jj, t):
    """vectorized distance between fleet pairs (ii,jj) at times t (same shape)."""
    def one(idx):
        M = np.mod(M0[idx] + (a[idx] ** -1.5) * t, TAU)
        E = kepler_E(e[idx], M)
        r = a[idx] * (1.0 - e[idx] * np.cos(E))
        nu = 2.0 * np.arctan2(np.sqrt(1 + e[idx]) * np.sin(E),
                               np.sqrt(1 - e[idx]) * np.cos(E))
        lt = pom[idx] + nu
        return r * np.cos(lt), r * np.sin(lt)
    xi, yi = one(ii)
    xj, yj = one(jj)
    return np.hypot(xi - xj, yi - yj)


def refine_pairs(a, e, pom, M0, ii, jj, t0, dt_win, iters=50):
    lo = np.maximum(0.0, t0 - dt_win)
    hi = t0 + dt_win
    for _ in range(iters):
        m1 = lo + (hi - lo) / 3.0
        m2 = hi - (hi - lo) / 3.0
        closer = pair_dist(a, e, pom, M0, ii, jj, m1) < pair_dist(a, e, pom, M0, ii, jj, m2)
        hi = np.where(closer, m2, hi)
        lo = np.where(closer, lo, m1)
    tm = 0.5 * (lo + hi)
    return tm, pair_dist(a, e, pom, M0, ii, jj, tm)


def lin_rank(lams, i, j):
    """rank of j among all, keyed by circular arc to i's longitude."""
    d = np.abs((lams - lams[i] + np.pi) % TAU - np.pi)
    return int((d < d[j] - 1e-15).sum())


def run_case(name, nc, a_hw, sig_lam, sig_e, seed, orbits=2.0, rank_sample=4000, pom_spread=0.1):
    a, e, pom, M0 = make_fleet(nc, a_hw, sig_lam, sig_e, seed, pom_spread=pom_spread)
    v_est = 3.0 * a_hw + 2.5 * max(E_CAP, 3 * sig_e)
    dt = min(0.05, 0.25 * RHO / v_est)
    T = orbits * TAU
    t_start = time.time()
    best_d, best_t = grid_min(a, e, pom, M0, T, dt)
    t_grid = time.time() - t_start
    iu, ju = np.triu_indices(nc, 1)
    sel = best_d[iu, ju] < 6 * RHO
    ii, jj = iu[sel], ju[sel]
    tm, dm = refine_pairs(a, e, pom, M0, ii, jj, best_t[ii, jj], dt)
    keep = dm < RHO
    ii, jj, tm, dm = ii[keep], jj[keep], tm[keep], dm[keep]
    n_contacts = ii.size
    rng = np.random.default_rng(seed + 999)
    if n_contacts > rank_sample:
        s = rng.choice(n_contacts, rank_sample, replace=False)
        sampled = True
    else:
        s = np.arange(n_contacts)
        sampled = False
    rows = []
    # pile size at t=0: ships within 2*rho of each ship (watch-list demand)
    pos0, lt0, _ = states(a, e, pom, M0, np.array([0.0]))
    xy0 = pos0[:, 0, :]
    d0 = np.sqrt(((xy0[:, None, :] - xy0[None, :, :]) ** 2).sum(-1))
    within2 = (d0 < 2 * RHO).sum(1) - 1
    for k in s:
        i, j = int(ii[k]), int(jj[k])
        pos, lt, lm = states(a, e, pom, M0, np.array([tm[k]]))
        xy, lt, lm = pos[:, 0, :], lt[:, 0], lm[:, 0]
        dd_i = np.sqrt(((xy - xy[i]) ** 2).sum(1))
        dd_j = np.sqrt(((xy - xy[j]) ** 2).sum(1))
        rk_d = min(int((dd_i < dd_i[j] - 1e-15).sum()), int((dd_j < dd_j[i] - 1e-15).sum()))
        rk_lt = min(lin_rank(lt, i, j), lin_rank(lt, j, i))
        rk_lm = min(lin_rank(lm, i, j), lin_rank(lm, j, i))
        # entry rank: partner's distance-rank when the pair first comes within 2*rho
        # (bisection on d(t) between t* and the last grid time with d >= 2*rho; pairs
        # inside 2*rho from t=0 are 'born in pile', ranked at t=0)
        born = bool(d0[i, j] < 2 * RHO)
        if born:
            te = 0.0
            xy_e = xy0
        else:
            tg = tm[k]
            d_pair = lambda t: pair_dist(a, e, pom, M0, np.array([i]), np.array([j]), np.array([t]))[0]
            step = max(dt, 1e-4)
            while tg > 0 and d_pair(max(0.0, tg - step)) < 2 * RHO:
                tg = max(0.0, tg - step)
            lo_e, hi_e = max(0.0, tg - step), tg
            for _ in range(40):
                mid = 0.5 * (lo_e + hi_e)
                if d_pair(mid) < 2 * RHO:
                    hi_e = mid
                else:
                    lo_e = mid
            te = hi_e
            pos_e, lt_e, _ = states(a, e, pom, M0, np.array([te]))
            xy_e = pos_e[:, 0, :]
        de_i = np.sqrt(((xy_e - xy_e[i]) ** 2).sum(1))
        de_j = np.sqrt(((xy_e - xy_e[j]) ** 2).sum(1))
        rk_entry = min(int((de_i < de_i[j] - 1e-15).sum()), int((de_j < de_j[i] - 1e-15).sum()))
        rows.append(dict(pair=[i, j], d=float(dm[k]), t=float(tm[k]), t_entry=float(te),
                         born_in_pile=born, rank_d=rk_d, rank_lt=rk_lt, rank_lm=rk_lm,
                         rank_entry=rk_entry))
    rd = np.array([r["rank_d"] for r in rows]) if rows else np.array([0])
    re_ = np.array([r["rank_entry"] for r in rows]) if rows else np.array([0])
    rt = np.array([r["rank_lt"] for r in rows]) if rows else np.array([0])
    rm = np.array([r["rank_lm"] for r in rows]) if rows else np.array([0])
    lam_sigma = sig_lam if sig_lam > 0 else TAU / np.sqrt(2 * np.pi)
    Pi = 2 * RHO * nc / (lam_sigma * np.sqrt(2 * np.pi))
    return dict(case=name, nc=nc, a_hw=a_hw, sig_lam=sig_lam, sig_e=sig_e, seed=seed,
                orbits=orbits, dt=dt, grid_s=round(t_grid, 1), contacts=int(n_contacts),
                ranked=len(rows), sampled=bool(sampled), Pi=Pi,
                pile2rho_max=int(within2.max()), pile2rho_mean=float(within2.mean()),
                born_in_pile=int(sum(r["born_in_pile"] for r in rows)),
                rank_d_max=int(rd.max()), rank_d_p99=float(np.percentile(rd, 99)) if len(rows) else 0.0,
                rank_d_over4=int((rd > 4).sum()), rank_d_over8=int((rd > 8).sum()),
                rank_entry_max=int(re_.max()), rank_entry_p99=float(np.percentile(re_, 99)) if len(rows) else 0.0,
                rank_entry_over4=int((re_ > 4).sum()), rank_entry_over8=int((re_ > 8).sum()),
                rank_lt_max=int(rt.max()), rank_lt_over4=int((rt > 4).sum()),
                rank_lm_max=int(rm.max()), rank_lm_over4=int((rm > 4).sum()),
                d_min=float(min((r["d"] for r in rows), default=float("nan")))), rows


CASES = [
    ("control", 200, 1e-5, 1e-2, 1e-3, 31),
    ("control", 200, 1e-5, 1e-2, 1e-3, 32),
    ("jam3e-3", 200, 1e-5, 3e-3, 1e-3, 31),
    ("jam3e-3", 200, 1e-5, 3e-3, 1e-3, 32),
    ("jam1e-3", 200, 1e-5, 1e-3, 1e-3, 31),
    ("jam1e-3", 200, 1e-5, 1e-3, 1e-3, 32),
    ("jam1e-3", 200, 1e-5, 1e-3, 1e-3, 33),
    ("jam3e-4", 200, 1e-5, 3e-4, 1e-3, 31),
    ("jam3e-4", 200, 1e-5, 3e-4, 1e-3, 32),
    ("scale800", 800, 1e-5, 1e-3, 1e-3, 41),
    ("scale800", 800, 1e-5, 1e-3, 1e-3, 42),
    ("espread", 200, 1e-5, 1e-3, 5e-3, 51),
    ("espread", 200, 1e-5, 1e-3, 5e-3, 52),
]

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "main"
    sel = [c for c in CASES if which == "main" or c[0] == which]
    summary, detail = [], []
    for name, nc, a_hw, sl, se, seed in sel:
        out, rows = run_case(name, nc, a_hw, sl, se, seed)
        summary.append(out)
        detail.extend(rows)
        print(json.dumps(out), flush=True)
    with open(f"probe-{which}-out.json", "w") as f:
        json.dump(dict(summary=summary, contacts=detail), f)
    print("wrote probe-%s-out.json" % which)
