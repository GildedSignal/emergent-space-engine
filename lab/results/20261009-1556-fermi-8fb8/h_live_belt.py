#!/usr/bin/env python3
"""H_live in a belt: program + scars under a Poisson stream of encounter kicks.

Model (docs/law.md populations): bodies stored as (population, ordinal); the
law's element quantum delta. Encounters are a Poisson stream of impulsive
kicks. Measured branches:
  H_A        : per-body deviation from the frozen program (identity-tied
               bodies only) — the random-walk field at delta.
  H_multiset : what the multiset costs beyond a 2-param refit program when
               the identity of interchangeable bodies is given up at
               recompile (permutation gauge): entropy of the sorted-vs-refit
               quantile residual at delta.
Controls: Gaussian kernel (analytic law), no-program direct store.
"""
import json
import sys

import numpy as np


def h_bits(x, delta):
    """Plug-in entropy (bits/sample) of a 1-D field at quantum delta, Miller-Madow corrected."""
    # grid anchored at absolute 0 so the delta and delta/2 grids nest exactly
    idx = np.floor(x / delta).astype(np.int64)
    c = np.bincount(idx - idx.min()).astype(np.float64)
    n = c.sum()
    p = c[c > 0] / n
    m = len(p)
    return float(-(p * np.log2(p)).sum() + (m - 1) / (2.0 * n * np.log(2.0)))


def h_bits2(x, y, dx, dy):
    """Joint entropy of two fields at quanta dx, dy (memory-safe via unique)."""
    ix = np.floor((x - (x.min() - dx)) / dx).astype(np.int64)
    iy = np.floor((y - (y.min() - dy)) / dy).astype(np.int64)
    keys = ix * (iy.max() + 1) + iy
    _, c = np.unique(keys, return_counts=True)
    c = c.astype(np.float64)
    n = c.sum()
    p = c / n
    m = len(p)
    return float(-(p * np.log2(p)).sum() + (m - 1) / (2.0 * n * np.log(2.0)))


def kicks(rng, n, kernel, s1):
    if kernel == "gauss":
        return rng.standard_normal(n) * s1
    # Rutherford: b = b_max*sqrt(u), deflection ~ 1/b -> kick = C/sqrt(u),
    # u ~ U(u_min,1), calibrated so median kick = s1. Tail index 2, range 100x.
    u = rng.uniform(1e-4, 1.0, n)
    k = (s1 / np.sqrt(2.0)) / np.sqrt(u)
    k *= np.where(rng.random(n) < 0.5, 1.0, -1.0)
    return k


def run(seed, kernel, s0=1.0, s1=1.0 / 64.0, delta=None, lam=1.0,
        epochs=8192, n=1 << 16, checkpoints=None, twodim=False):
    rng = np.random.default_rng(seed)
    if delta is None:
        delta = s1 / 8.0
    if checkpoints is None:
        checkpoints = [1 << j for j in range(0, 14)]
    # program: stratified exact individuals (B18-style: zero entropy at birth)
    q = (np.arange(n) + 0.5) / n
    from statistics import NormalDist
    _nd = NormalDist()
    erf_inv = np.vectorize(lambda v: _nd.inv_cdf(0.5 * (v + 1.0)), otypes=[float])
    gen = s0 * erf_inv(2.0 * q - 1.0)  # erf_inv already returns Phi^-1(q)
    walk = np.zeros(n)
    walk2 = np.zeros(n)  # second element, correlated kicks (2-D check)
    out = []
    ep = 0
    ks = set(sorted(checkpoints))
    while ep < epochs:
        cnt = rng.poisson(lam, n)
        tot = int(cnt.sum())
        body = np.repeat(np.arange(n), cnt)
        if not twodim:
            kk = kicks(rng, tot, kernel, s1)
            np.add.at(walk, body, kk)
        else:
            # one encounter kicks both elements; Gaussian case rho = -0.6,
            # Rutherford case: shared amplitude, independent signs (rho ~ 0)
            if kernel == "gauss":
                rho = -0.6
                z0 = rng.standard_normal(tot)
                z1 = z0
                z2 = rho * z0 + np.sqrt(1 - rho * rho) * rng.standard_normal(tot)
                k1, k2 = z1 * s1, z2 * s1
            else:
                u = rng.uniform(1e-4, 1.0, tot)
                amp = (s1 / np.sqrt(2.0)) / np.sqrt(u)
                k1 = amp * np.where(rng.random(tot) < 0.5, 1.0, -1.0)
                k2 = amp * np.where(rng.random(tot) < 0.5, 1.0, -1.0)
            np.add.at(walk, body, k1)
            np.add.at(walk2, body, k2)
        ep += 1
        if ep in ks:
            actual = gen + walk
            rec = {"k": ep, "seed": seed, "kernel": kernel}
            rec["H_A"] = h_bits(walk, delta)
            rec["H_A_d2"] = h_bits(walk, delta / 2)
            rec["H_A_2d"] = h_bits2(walk, walk2, delta / 2, delta / 2) if twodim else None
            # multiset branch (permutation gauge): sort-match actuals against the
            # refit program family (2-param normal); identity of interchangeable
            # is given up at recompile. Cost = entropy of the quantile residual.
            order = np.argsort(actual)
            mu = float(actual.mean())
            shat = float(np.sqrt(np.mean((actual - mu) ** 2)))
            qhat = mu + shat * erf_inv(2.0 * q - 1.0)
            residm = np.sort(actual) - qhat
            rec["H_multiset"] = h_bits(residm, delta)
            rec["sigma_hat"] = shat
            # control: no program, direct store of actuals at delta
            rec["H_noprog"] = h_bits(actual, delta)
            rec["sigma_k"] = float(np.std(walk))
            out.append(rec)
    return out


def _erfinv_cache(v):
    from math import erfinv
    return erfinv(v)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "main"
    if mode == "main":  # seed 1 (tuning seed), both kernels, 1-D
        for kern in ("gauss", "rutherford"):
            res = run(1, kern)
            for r in res:
                r["mode"] = "main"
            with open(f"mc_seed1_{kern}.json", "w") as f:
                json.dump(res, f, indent=1)
            print(kern, "done", len(res), "checkpoints")
    elif mode == "heldout":  # seeds 2 and 3
        for kern in ("gauss", "rutherford"):
            for seed in (2, 3):
                res = run(seed, kern)
                with open(f"mc_seed{seed}_{kern}.json", "w") as f:
                    json.dump(res, f, indent=1)
                print(kern, seed, "done")
    elif mode == "twodim":
        res = run(1, "gauss", twodim=True)
        with open("mc_2d_gauss.json", "w") as f:
            json.dump(res, f, indent=1)
        res = run(1, "rutherford", twodim=True)
        with open("mc_2d_rutherford.json", "w") as f:
            json.dump(res, f, indent=1)
        print("2d done")
    elif mode == "kickentropy":
        rng = np.random.default_rng(11)
        s1 = 1.0 / 64.0
        for kern in ("gauss", "rutherford"):
            kk = kicks(rng, 1 << 20, kern, s1)
            print(kern, "h_kick@delta:", h_bits(kk, s1 / 8.0),
                  "median", float(np.median(np.abs(kk))), "max", float(np.max(np.abs(kk))))
