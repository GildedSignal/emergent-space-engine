#!/usr/bin/env python3
"""Inversion of gold 20261006-0346-taleb-09b5: does the k=4 phase-neighbour train
certificate survive packing (ships per rho of along-track arc)?

Instrument mirrors their taleb.rs: brute-force dense sampling, per-pair global min
distance < RHO, partner's 3D distance-rank at that instant (min over both
directions, # ships strictly closer). Adds: circular longitude-rank, simultaneous
sub-rho multiplicity. Units: a~1, mu=1 (period 2pi), RHO=1e-4.
"""
import json, sys
import numpy as np

RHO = 1e-4
TAU = 2 * np.pi
rng_global = np.random.default_rng(20261007)


def kepler_pos_circ(a, M0, n, t):
    th = M0[None, :] + n[None, :] * t[:, None]
    r = a[None, :]
    return np.stack([r * np.cos(th), r * np.sin(th)], axis=-1)  # (T,N,2)


def kepler_pos_e(a, e, pom, M0, n, t):
    """First-order in e (e<=0.01 => O(e^2)~1e-4 relative on the breathing, 0.01*rho abs)."""
    M = M0[None, :] + n[None, :] * t[:, None]
    r = a[None, :] * (1 - e[None, :] * np.cos(M))
    th = M + pom[None, :] + 2 * e[None, :] * np.sin(M)
    return np.stack([r * np.cos(th), r * np.sin(th)], axis=-1)


def run_scene(name, N, packing=None, a_hw_rho=0.3, sig_lam=None, e_scale=0.0,
              pom_hw=0.0, orbits=20.0, dt=0.05, seed=None, uniform_arc=True):
    rng = np.random.default_rng(seed if seed is not None else 7)
    if uniform_arc:
        s = RHO / packing                 # mean along-track spacing
        arc = N * s
        lam0 = rng.uniform(-arc / 2, arc / 2, N)
    else:                                  # gaussian phalanx (their family)
        lam0 = rng.normal(0.0, sig_lam, N)
    a = 1.0 + rng.uniform(-a_hw_rho, a_hw_rho, N) * RHO
    n = a ** -1.5
    if e_scale > 0:
        e = rng.rayleigh(e_scale, N)
        pom = rng.uniform(-pom_hw, pom_hw, N)
        posf = lambda t: kepler_pos_e(a, e, pom, lam0, n, t)
    else:
        posf = lambda t: kepler_pos_circ(a, lam0, n, t)

    T = np.arange(0.0, orbits * TAU, dt)
    ii, jj = np.triu_indices(N, k=1)
    pairmin = np.full(ii.size, np.inf)
    pairarg = np.zeros(ii.size, dtype=np.int64)
    B = 100
    for b0 in range(0, T.size, B):
        tb = T[b0:b0 + B]
        P = posf(tb)                                  # (B,N,2)
        d = P[:, ii, :] - P[:, jj, :]                 # (B,npairs,2)
        D = np.hypot(d[..., 0], d[..., 1])
        m = D.min(axis=0); am = D.argmin(axis=0)
        upd = m < pairmin
        pairmin[upd] = m[upd]
        pairarg[upd] = b0 + am[upd]

    enc = np.where(pairmin < RHO)[0]
    # group encounters by their t* step
    steps = pairarg[enc]
    order = np.argsort(steps, kind='stable')
    enc, steps = enc[order], steps[order]
    bounds = np.searchsorted(steps, np.arange(T.size + 1))

    r_arr, lr_arr, mult_arr, dmin_arr = [], [], [], []
    for st in np.unique(steps):
        i0, i1 = bounds[st], bounds[st + 1]
        if i0 == i1:
            continue
        seg = enc[i0:i1]
        I, J = ii[seg], jj[seg]
        P = posf(np.array([T[st]]))[0]                # (N,2)
        Dm = np.hypot(P[:, 0][:, None] - P[:, 0][None, :],
                      P[:, 1][:, None] - P[:, 1][None, :])
        dij = Dm[I, J]
        rI = (Dm[I, :] < dij[:, None]).sum(1) - 1     # -1: self (d=0)
        rJ = (Dm[J, :] < dij[:, None]).sum(1) - 1
        r_arr.append(np.minimum(rI, rJ))
        mI = (Dm[I, :] < RHO).sum(1) - 1
        mJ = (Dm[J, :] < RHO).sum(1) - 1
        mult_arr.append(np.maximum(mI, mJ))
        th = np.arctan2(P[:, 1], P[:, 0])
        def circ(x):
            return np.abs((x + np.pi) % TAU - np.pi)
        cij_i = circ(th[J] - th[I]); cij_j = circ(th[I] - th[J])
        lI = (circ(th[None, :] - th[I][:, None])[:, :] < cij_i[:, None]).sum(1) - 1
        lJ = (circ(th[None, :] - th[J][:, None])[:, :] < cij_j[:, None]).sum(1) - 1
        lr_arr.append(np.minimum(lI, lJ))
        dmin_arr.append(dij)

    r = np.concatenate(r_arr) if r_arr else np.array([], int)
    lr = np.concatenate(lr_arr) if lr_arr else np.array([], int)
    mu_ = np.concatenate(mult_arr) if mult_arr else np.array([], int)
    dm = np.concatenate(dmin_arr) if dmin_arr else np.array([])
    out = {
        "scene": name, "N": N,
        "packing_pi": (packing if packing else None),
        "sig_lam": sig_lam, "e_scale": e_scale, "a_hw_rho": a_hw_rho,
        "orbits": orbits, "encounters": int(r.size),
        "r_max": int(r.max()) if r.size else None,
        "r_p99": int(np.percentile(r, 99)) if r.size else None,
        "frac_r_gt4": float((r > 4).mean()) if r.size else None,
        "frac_r_gt8": float((r > 8).mean()) if r.size else None,
        "lr_max": int(lr.max()) if lr.size else None,
        "frac_lr_gt4": float((lr > 4).mean()) if lr.size else None,
        "mult_max": int(mu_.max()) if mu_.size else None,
        "mult_median": float(np.median(mu_)) if mu_.size else None,
        "dmin_med": float(np.median(dm)) if dm.size else None,
    }
    print(json.dumps(out), flush=True)
    return out, r, lr, mu_


if __name__ == "__main__":
    results = []
    # P1: instrument calibration — their tightest phalanx family (sigma_lam=0.01, a_hw=1e-5, e Rayleigh 1e-3, pom ±0.1)
    results.append(run_scene("calib-e-their-phalanx", N=200, sig_lam=0.01, a_hw_rho=0.1,
                             e_scale=1e-3, pom_hw=0.1, uniform_arc=False,
                             orbits=6.0, dt=0.005, seed=27)[0])
    # P2: uniform packing at their measured boundary
    results.append(run_scene("circ-pi0.8", N=240, packing=0.8, seed=1)[0])
    # P3-P5: the packing sweep (the game's concentrated fleet, scaled to lab size)
    for pi in (2, 4, 8):
        results.append(run_scene(f"circ-pi{pi}", N=240, packing=pi, seed=1)[0])
    # P6: their own flagged worry — e-spread breathing 100*rho at loose packing
    results.append(run_scene("spread-e-pi0.5", N=240, packing=0.5, e_scale=1e-2,
                             pom_hw=0.1, orbits=6.0, dt=0.005, seed=5)[0])
    with open(sys.argv[1] if len(sys.argv) > 1 else "packing-results.json", "w") as f:
        json.dump(results, f, indent=1)
