#!/usr/bin/env python3
"""taleb-e013: does the phase-neighbour train certificate's k stay constant?

Attack on gold 20261006-0346-taleb-09b5: it measured distance-rank <= 4 at
n_c <= 800 and proposed a longitude-sorted train watching k~4 neighbours.
At a sub-rho contact |dlambda| <= d_min, so the bodies with true longitude
between the two partners (lambda inside the contact window, radially far)
consume watch slots: required k ~ 2*d_min * true-longitude line density,
which scales linearly with n_c at fixed spread.

Truth: per-step 2D KD-tree detection (no longitude binning). Ranks at each
encounter's argmin step:
  lam-rank  : |idx_i - idx_j| in the true-longitude-sorted order (the train)
  dist-rank : # bodies closer to i than partner j is (the gold's measurement)
Coplanar fleet on one orbit: a=1+U(-a_hw,a_hw), e~Rayleigh(1e-3), rho=1e-4.
lam = ("uniform",) | ("gauss", sigma_lam) | ("gauss", sigma_lam, sigma_varpi)
"""
import json, sys, time
import numpy as np
from scipy.spatial import cKDTree

RHO = 1e-4
A_HW, E_SCALE, VARPI_B = 1e-5, 1e-3, 0.1

def kepler_positions(M, e, a, varpi):
    E = M.copy()
    for _ in range(8):
        E -= (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    x = a * (np.cos(E) - e)
    y = a * np.sqrt(1.0 - e * e) * np.sin(E)
    c, s = np.cos(varpi), np.sin(varpi)
    return np.stack([x * c - y * s, x * s + y * c], axis=1)

def make(n, lam, seed):
    rng = np.random.default_rng(seed)
    if lam[0] == "uniform":
        M0 = rng.uniform(0.0, 2.0 * np.pi, n)
    else:
        M0 = rng.normal(np.pi, lam[1], n)
    e = rng.rayleigh(E_SCALE, n)
    a = 1.0 + rng.uniform(-A_HW, A_HW, n)
    if len(lam) > 2:  # (gauss, sigma_lam, sigma_varpi): aligned formation
        varpi = rng.normal(0.0, lam[2], n)
    else:
        varpi = rng.uniform(-VARPI_B, VARPI_B, n)
    return M0, e, a, varpi

def run_case(name, n, lam, orbits, S, seed, det_mult=1.3, rank_cap=2500):
    t0 = time.time()
    lam_lbl = repr(lam)
    M0, e, a, varpi = make(n, lam, seed)
    nsteps = orbits * S
    best = {}
    maxpairstep = 0
    for step in range(nsteps):
        pos = kepler_positions(M0 + step * 2.0 * np.pi / S, e, a, varpi)
        pairs = cKDTree(pos).query_pairs(det_mult * RHO, output_type="ndarray")
        maxpairstep = max(maxpairstep, len(pairs))
        if len(pairs):
            d = np.hypot(*(pos[pairs[:, 0]] - pos[pairs[:, 1]]).T)
            for (i, j), dij in zip(pairs, d):
                key = (int(i), int(j))
                old = best.get(key)
                if old is None or dij < old[0]:
                    best[key] = (float(dij), step)
    enc = {k: v for k, v in best.items() if v[0] < RHO}
    bystep = {}
    for (i, j), (d, step) in enc.items():
        bystep.setdefault(step, []).append((i, j, d))
    lam_r, dr_max, dr_min, dmins = [], [], [], []
    done = 0
    for step, evs in sorted(bystep.items()):
        if done >= rank_cap:
            break
        pos = kepler_positions(M0 + step * 2.0 * np.pi / S, e, a, varpi)
        lam = np.arctan2(pos[:, 1], pos[:, 0])
        inv = np.empty(n, dtype=np.int64)
        inv[np.argsort(lam)] = np.arange(n)
        for (i, j, d) in evs:
            if done >= rank_cap:
                break
            lam_r.append(abs(int(inv[i]) - int(inv[j])))
            di = np.hypot(*(pos - pos[i]).T); di[i] = np.inf
            dj = np.hypot(*(pos - pos[j]).T); dj[j] = np.inf
            ri = int((di < d).sum()); rj = int((dj < d).sum())
            dr_max.append(max(ri, rj)); dr_min.append(min(ri, rj))
            dmins.append(d); done += 1
    lam_r = np.array(lam_r); dr_max = np.array(dr_max); dr_min = np.array(dr_min)
    dmins = np.array(dmins)
    out = dict(
        case=name, n=n, lam=lam_lbl, orbits=orbits, S=S, seed=seed,
        n_enc=len(enc), ranked=done, max_pairs_per_step=maxpairstep,
        enc_rate_per_body_orbit=round(len(enc) / n / orbits, 4),
        lam_mu_hat=float((lam_r - 1).mean()) if done else 0.0,
        lam_p50=float(np.percentile(lam_r, 50)) if done else -1,
        lam_p90=float(np.percentile(lam_r, 90)) if done else -1,
        lam_p99=float(np.percentile(lam_r, 99)) if done else -1,
        lam_max=int(lam_r.max()) if done else -1,
        dist_p50=float(np.percentile(dr_max, 50)) if done else -1,
        dist_p90=float(np.percentile(dr_max, 90)) if done else -1,
        dist_max=int(dr_max.max()) if done else -1,
        dmin_med=float(np.median(dmins)) if done else -1,
        miss_lam_k4=float((lam_r > 4).mean()) if done else -1,
        miss_lam_k8=float((lam_r > 8).mean()) if done else -1,
        miss_dist_k4=float((dr_min > 4).mean()) if done else -1,
        wall_s=round(time.time() - t0, 1),
    )
    return out, best

def main():
    cases = [
        ("C0-anchor",   200,    ("gauss", 0.01),  1, 512,  27),
        ("C0-anchor-hi", 200,   ("gauss", 0.01),  1, 1024, 27),
        ("C1-uniform",  800,    ("uniform",),     20, 256,  1),
        ("C2a-bunch",   800,    ("gauss", 0.004), 3, 256,  2),
        ("C2b-bunch",   800,    ("gauss", 0.0015),3, 256,  3),
        ("C2c-bunch",   800,    ("gauss", 0.0005),3, 256,  4),
        ("C3a-uniform", 12800,  ("uniform",),      3, 128,  5),
        ("C3b-uniform", 51200,  ("uniform",),      3, 128,  6),
        ("C3c-uniform", 128000, ("uniform",),      2, 128,  7),
        ("D1-aligned",  800,    ("gauss", 0.012, 0.012), 3, 256, 11),
        ("D2-aligned",  800,    ("gauss", 0.008, 0.008), 3, 256, 12),
        ("D3-aligned",  800,    ("gauss", 0.004, 0.004), 3, 256, 13),
        ("X1-uniform",  256000, ("uniform",),        2, 128,  14),
    ]
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    try:
        results = json.load(open(__file__.replace("probe.py", "results.json")))
    except Exception:
        results = []
    have = {r["case"] for r in results}
    for c in cases:
        if only and c[0] not in only:
            continue
        out, _ = run_case(*c)
        results = [r for r in results if r["case"] != c[0]] + [out]
        print(json.dumps(out), flush=True)
    if not only or any(k in only for k in ("C0-anchor", "C0-anchor-hi")):
        _, lo = run_case("nest-lo", 200, ("gauss", 0.01), 1, 512, 27)
        _, hi = run_case("nest-hi", 200, ("gauss", 0.01), 1, 1024, 27)
        lset = {k for k, v in lo.items() if v[0] < RHO}
        hset = {k for k, v in hi.items() if v[0] < RHO}
        print(json.dumps(dict(nest_check=dict(
            s512=len(lset), s1024=len(hset), shared=len(lset & hset),
            frac=round(len(lset & hset) / max(1, len(lset)), 4)))), flush=True)
    with open(__file__.replace("probe.py", "results.json"), "w") as f:
        json.dump(sorted(results, key=lambda r: r["case"]), f, indent=1)

if __name__ == "__main__":
    main()
