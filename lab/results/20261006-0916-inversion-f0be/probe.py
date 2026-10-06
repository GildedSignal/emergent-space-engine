#!/usr/bin/env python3
"""inversion-f0be: does the phase-neighbour 'train' certificate (taleb-09b5, gold)
break inside its own trigger regime? Exact-Kepler toy, a=1 for all bodies
(tighter than the gold's fleet => exactly periodic, generous to the train).

Truth contacts, rank-assumption-free:
  1) ALL n(n-1)/2 pairs screened on T t-nodes with the rigorous lower bound
     LB^2 = (r_i-r_j)^2 + r_i r_j dl^2 (2/pi)^2  (chord >= (2/pi)arc, |dl|<=pi/2);
     candidate iff min_t LB < 3 rho.
  2) candidates sampled densely (512 nodes/orbit), local minima < 5 rho refined
     on a 129-point grid, then a 65-point second stage.
Ranks at contact use exact geometry at the refined time under PERFECT continuous
maintenance (the train's best case). Overtakes/orbit = Kendall distance of the
longitude ring between consecutive samples."""
import numpy as np, json, sys

RHO = 1e-4
S = 4096                      # ring-order samples per orbit (uniform in time)
TWO_PI = 2 * np.pi

def kepler(M, e):
    E = M + e * np.sin(M)
    for _ in range(30):
        g = E - e * np.sin(E) - M
        E = E - g / (1 - e * np.cos(E))
    return E

def pos_from_E(E, e, pi):
    r = 1.0 - e * np.cos(E)
    cf = (np.cos(E) - e) / r
    sf = np.sqrt(1 - e * e) * np.sin(E) / r
    f = np.arctan2(sf, cf)
    lam = pi + f
    return r * np.cos(lam), r * np.sin(lam), r, lam, f

def positions(M, e, pi):
    shape = np.broadcast_shapes(M.shape, e.shape, pi.shape)
    E = kepler(np.broadcast_to(M, shape), np.broadcast_to(e, shape))
    return pos_from_E(E, np.broadcast_to(e, shape), np.broadcast_to(pi, shape))

def rayleigh(n, sigma, rng):
    return sigma * np.sqrt(-2 * np.log(rng.random(n)))

def run_scene(tag, n, e0, esig, sig_M, seed=27, pi_spread=0.1, report_anom=False):
    rng = np.random.default_rng(seed)
    e = e0 + rayleigh(n, esig, rng)
    pi = rng.uniform(-pi_spread, pi_spread, n)
    M0 = (rng.normal(0, sig_M, n)) % TWO_PI

    dM = TWO_PI / S
    # --- ring order history + min instantaneous spacing ---
    rank_hist = np.empty((S, n), dtype=np.int32)
    min_nn_arc = np.inf
    for c0 in range(0, S, 256):
        c1 = c0 + 256
        Mc = (np.arange(c0, c1) * dM)[:, None] + M0[None, :]
        x, y, r, lam, _ = positions(Mc, e[None, :], pi[None, :])
        order = np.argsort(lam, axis=1)
        rk = np.empty_like(order)
        np.put_along_axis(rk, order, np.broadcast_to(np.arange(n), order.shape), axis=1)
        rank_hist[c0:c1] = rk
        lu = np.take_along_axis(lam, order, axis=1)
        ru = np.take_along_axis(r, order, axis=1)
        arc = (lu - np.roll(lu, 1, axis=1)) % TWO_PI * np.sqrt(ru * np.roll(ru, 1, axis=1))
        min_nn_arc = min(min_nn_arc, np.min(arc))

    # --- candidate gate: all pairs, rigorous LB on T nodes (30 rho) ---
    T = 256
    tt = np.arange(T) * (TWO_PI / T)
    ii, jj = np.triu_indices(n, 1)
    keep = np.zeros(len(ii), dtype=bool)
    for t0 in range(0, T, 32):
        t1 = t0 + 32
        Mc = tt[t0:t1, None] + M0[None, :]
        x, y, r, lam, _ = positions(Mc, e[None, :], pi[None, :])
        ri = r[:, ii]; rj = r[:, jj]
        dl = np.abs((lam[:, ii] - lam[:, jj] + np.pi) % TWO_PI - np.pi)
        dl = np.minimum(dl, TWO_PI - dl)
        LB2 = (ri - rj) ** 2 + ri * rj * (dl * 2 / np.pi) ** 2
        keep |= (LB2 < (30 * RHO) ** 2).any(axis=0)
    ci_, cj_ = ii[keep], jj[keep]
    C0 = len(ci_)

    # --- 8192-node running min per candidate pair, then 3-centre refinement ---
    W = 8192
    dw = TWO_PI / W
    best_d = np.full(C0, np.inf); best_w = np.zeros(C0, dtype=np.int64)
    for p0 in range(0, C0, 4000):
        p1 = min(p0 + 4000, C0)
        run = np.full(p1 - p0, np.inf); rw = np.zeros(p1 - p0, dtype=np.int64)
        for w0 in range(0, W, 1024):
            w1 = w0 + 1024
            Mc = (np.arange(w0, w1) * dw)[:, None] + M0[None, ci_[p0:p1]]
            x, y, r, lam, _ = positions(Mc, e[None, ci_[p0:p1]], pi[None, ci_[p0:p1]])
            x2 = x - x * 0  # placeholder to keep shapes clear
            Mc2 = (np.arange(w0, w1) * dw)[:, None] + M0[None, cj_[p0:p1]]
            xj, yj, _, _, _ = positions(Mc2, e[None, cj_[p0:p1]], pi[None, cj_[p0:p1]])
            d = np.hypot(x - xj, y - yj)                  # (w-chunk, P-chunk)
            k = d.argmin(axis=0)
            m = d[k, np.arange(p1 - p0)]
            upd = m < run
            run[upd] = m[upd]; rw[upd] = w0 + k[upd]
        best_d[p0:p1] = run; best_w[p0:p1] = rw
    # refine around argmin node and both neighbours (covers boundary + shoulder)
    mstar = np.zeros(C0)
    for p0 in range(0, C0, 20000):
        p1 = min(p0 + 20000, C0)
        bi, bj = ci_[p0:p1], cj_[p0:p1]
        for off in (-1, 0, 1):
            g = ((best_w[p0:p1] + off) * dw + M0[bi])[:, None] + np.linspace(-2 * dw, 2 * dw, 129)[None, :]
            gj = g + (M0[bj] - M0[bi])[:, None]
            Ei = kepler(np.mod(g, TWO_PI), e[bi][:, None]); Ej = kepler(np.mod(gj, TWO_PI), e[bj][:, None])
            xi, yi, _, _, _ = pos_from_E(Ei, e[bi][:, None], pi[bi][:, None])
            xj, yj, _, _, _ = pos_from_E(Ej, e[bj][:, None], pi[bj][:, None])
            d = np.hypot(xi - xj, yi - yj)
            k = d.argmin(axis=1)
            d1 = d[np.arange(p1 - p0), k]; t1 = g[np.arange(p1 - p0), k] - M0[bi]
            g2 = (t1 + M0[bi])[:, None] + np.linspace(-2 * dw, 2 * dw, 65)[None, :]
            gj2 = g2 + (M0[bj] - M0[bi])[:, None]
            Ei = kepler(np.mod(g2, TWO_PI), e[bi][:, None]); Ej = kepler(np.mod(gj2, TWO_PI), e[bj][:, None])
            xi, yi, _, _, _ = pos_from_E(Ei, e[bi][:, None], pi[bi][:, None])
            xj, yj, _, _, _ = pos_from_E(Ej, e[bj][:, None], pi[bj][:, None])
            d = np.hypot(xi - xj, yi - yj)
            k = d.argmin(axis=1)
            d2 = d[np.arange(p1 - p0), k]; t2 = g2[np.arange(p1 - p0), k] - M0[bi]
            df = np.minimum(d1, d2); tf = np.where(d2 < d1, t2, t1)
            upd = df < best_d[p0:p1]
            best_d[p0:p1][upd] = df[upd]; mstar[p0:p1][upd] = tf[upd]

    contact = best_d < RHO
    C = int(contact.sum())
    out = {"tag": tag, "n": n, "e0": e0, "esig": esig, "sig_M": sig_M,
           "candidates": C0, "contacts": C, "min_nn_arc_over_orbit": float(min_nn_arc),
           "nominal_spacing_over_rho": float(2.5 * min(sig_M, TWO_PI) / n / RHO)}
    if C:
        ia, ja, ta = ci_[contact], cj_[contact], mstar[contact]
        ranks_l, ranks_d, anom_i, jam = [], [], [], []
        for t in range(0, C, 256):
            sl = slice(t, min(t + 256, C))
            Mc = ta[sl][:, None] + M0[None, :]
            xx, yy, rr, ll, ff = positions(Mc, e[None, :], pi[None, :])
            for a in range(sl.stop - sl.start):
                A, B = ia[sl][a], ja[sl][a]
                dd = np.hypot(xx[a] - xx[a, B], yy[a] - yy[a, B])
                dl = np.abs((ll[a] - ll[a, B] + np.pi) % TWO_PI - np.pi)
                mask = np.ones(n, dtype=bool); mask[A] = False
                ranks_d.append(int((dd[mask] < dd[B]).sum()) + 1)
                ranks_l.append(int((dl[mask] < dl[B]).sum()) + 1)
                jam.append(int((dd[mask] < RHO).sum()))
                anom_i.append(float(ff[a, A]))
        ranks_l = np.array(ranks_l); ranks_d = np.array(ranks_d); jam = np.array(jam)
        miss = ranks_l > 4
        out.update({"jam_max": int(jam.max()), "jam_median": float(np.median(jam)),
                    "max_rank_lam": int(ranks_l.max()), "p99_rank_lam": float(np.percentile(ranks_l, 99)),
                    "max_rank_dist": int(ranks_d.max()), "miss_rate_k4": float(miss.mean()),
                    "dmin_missed_min": float(best_d[contact][miss].min()) if miss.any() else None,
                    "dmin_missed_med": float(np.median(best_d[contact][miss])) if miss.any() else None})
        if report_anom:
            an = np.array(anom_i)
            out["anom_apo_frac_all"] = float(np.mean(np.abs(an - np.pi) < 0.5))
            out["anom_apo_frac_missed"] = float(np.mean(np.abs(an[miss] - np.pi) < 0.5)) if miss.any() else None
    overt = np.abs(np.diff(rank_hist, axis=0)).sum() / 2
    out["overtakes_per_orbit"] = float(overt)
    print(json.dumps(out), flush=True)
    return out

if __name__ == "__main__":
    results = []
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "s1"):
        results.append(run_scene("S1-control-gold-phalanx", 200, 0.0, 0.001, 0.01))
    if which in ("all", "s2"):
        for s in (0.01, 0.005, 0.002):
            results.append(run_scene(f"S2-jam-low-e s={s}", 512, 0.0, 0.001, s))
    if which in ("all", "s3"):
        for s in (0.04, 0.02, 0.01):
            results.append(run_scene(f"S3-dwell-e0.9 s={s}", 512, 0.9, 1e-5, s, report_anom=True))
    if which in ("all", "s4"):
        for n in (128, 512, 1024):
            results.append(run_scene(f"S4-maintenance n={n}", n, 0.3, 0.05, 10.0))  # sig_M=10 => uniform M0
    with open(f"results-{which}.json", "w") as f:
        json.dump(results, f, indent=1)
