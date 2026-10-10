#!/usr/bin/env python3
"""Gold rerun for 20261010-0306-spacex-acb2 (second author, run …-7b82).

Does exactly what the checker named:
  - >=5 seeds at 4000 pairs/bin under a hi-res instrument (512 coarse / 24 zoom
    pts / 6 rounds = the checker's parameters), plus an ultra-hi-res
    convergence control (2048/48/8) that was missing from the shipped run;
  - held-out belt widths W in {0.04, 0.1} (cold) to settle the closed form;
  - per-bin bmin/vrel/weight/P saved so post can bin-jackknife everything.

Physics and rate formula are the shipped probe's, imported unmodified; only
the instrument resolution, seed count and W grid change. Rates are computed
with the shipped rate_from_P (n1D = N/W, |dn| = 1.5*da).

Usage: gold_probe.py <job> <W> <sigma_e> <seed> <hires|ultra> <outprefix>
"""
import json
import sys
import time

import numpy as np

import probe_hlive as P
RES = {
    "hires": dict(n_coarse=512, n_zoom_pts=24, zoom_rounds=6),
    "ultra": dict(n_coarse=2048, n_zoom_pts=48, zoom_rounds=8),
    "xhi": dict(n_coarse=8192, n_zoom_pts=96, zoom_rounds=10),
}
RHOS = (1e-4, 1e-3, 1e-2)  # third rho: 2-decade exponent fit


def measure(W, sigma_e, N, bins, ppb, seed, res):
    """Shipped measure() with the instrument resolution exposed."""
    rng = np.random.default_rng(seed)
    da_max = 1.2 * (W + 4 * sigma_e)
    edges = np.geomspace(1e-5, da_max, bins + 1)
    out = {"edges": edges, "P": np.zeros((bins, len(RHOS))),
           "bmin": np.zeros((bins, ppb)), "vrel": np.zeros((bins, ppb)),
           "weight": np.zeros(bins)}
    for i in range(bins):
        lo, hi = edges[i], edges[i + 1]
        da = np.exp(rng.uniform(np.log(lo), np.log(hi), ppb))
        a1 = 1.0 + W * rng.random(ppb)
        a2 = a1 + da
        keep = a2 <= 1.0 + W
        out["weight"][i] = np.mean(keep)
        a1, a2, da = a1[keep], a2[keep], da[keep]
        m = len(a1)
        e1 = sigma_e * np.sqrt(-2.0 * np.log(1.0 - rng.random(m)))
        e2 = sigma_e * np.sqrt(-2.0 * np.log(1.0 - rng.random(m)))
        l1 = 2 * np.pi * rng.random(m)
        l2 = 2 * np.pi * rng.random(m)
        M01 = 2 * np.pi * rng.random(m)
        M02 = 2 * np.pi * rng.random(m)
        bmin, vrel = P.pair_min_distance(a1, e1, l1, M01, a2, e2, l2, M02, **res)
        out["bmin"][i, :m] = bmin
        out["vrel"][i, :m] = vrel
        for k, rho in enumerate(RHOS):
            out["P"][i, k] = np.mean(bmin < rho) if m else 0.0
    return out


def main():
    job, W, sigma_e, seed, res, outpref = (
        sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]),
        sys.argv[5], sys.argv[6])
    t0 = time.time()
    out = measure(W, sigma_e, N=1e4, bins=22, ppb=4000, seed=seed, res=RES[res])
    lams = {str(r): float(P.rate_from_P(out["edges"], out["P"][:, k], 1e4, W,
                                        weight=out["weight"]))
            for k, r in enumerate(RHOS)}
    np.savez_compressed(
        f"{outpref}_{job}.npz", edges=out["edges"], P=out["P"],
        weight=out["weight"], bmin=out["bmin"], vrel=out["vrel"])
    widest = float(np.max(out["P"][-2:, :]))
    rec = {"job": job, "W": W, "sigma_e": sigma_e, "seed": seed, "res": res,
           "Lambda": lams, "widest_bin_maxP": widest,
           "seconds": round(time.time() - t0, 1)}
    # encounter counts per rho from kept pairs
    kept = out["bmin"] > 0
    rec["n_enc_rho"] = {str(r): int((out["bmin"][kept] < r).sum()) for r in RHOS}
    print(json.dumps(rec), flush=True)


if __name__ == "__main__":
    main()
